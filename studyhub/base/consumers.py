
import json

from .models import Player
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.contenttypes.models import ContentType

from .models import Message


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        kwargs = self.scope['url_route']['kwargs']
        self.room_name = f"{kwargs['content_type']}_{kwargs['object_id']}"
        self.room_group_name = f'chat_{self.room_name}'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def fetch_messages(self, data):
        content_type = data['content_type']
        object_id = data['object_id']
        messages = Message.last_100_webinar_messages(content_type, object_id)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }

        self.send_json(content)

    def new_message(self, data):
        author = data['from']
        text = data['message']
        content_type = data['content_type']
        object_id = data['object_id']
        content_type = ContentType.objects.get(model=content_type)
        author_user = UserModel.objects.get(email=author)
        content_object = content_type.get_object_for_this_type(id=object_id)
        message = Message.objects.create(user=author_user, body=text, content_object=content_object)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    # Receive message from WebSocket
    def receive_json(self, content):
        self.commands[content['command']](self, content)

    def message_to_json(self, message):
        return {
            'id': str(message.id),
            'author': message.user.email,
            'content': message.body,
            'created': str(message.created)
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send_json(message)
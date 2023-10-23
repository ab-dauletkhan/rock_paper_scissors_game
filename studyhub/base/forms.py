from django.forms import ModelForm
from django.utils import timezone
from .models import Lobby


class LobbyForm(ModelForm):
    class Meta:
        model = Lobby
        fields = ['name', 'capacity']



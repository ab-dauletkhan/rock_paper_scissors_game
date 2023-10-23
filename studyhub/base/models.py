from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    total_games = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=50.0)
    last_online = models.DateTimeField(auto_now=True)
    current_lobby = models.ForeignKey('Lobby', on_delete=models.SET_NULL, null=True, blank=True)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


class Lobby(models.Model):
    name = models.CharField(max_length=200)
    host = models.ForeignKey(Player, on_delete=models.DO_NOTHING, null=True, related_name='hosted_lobbies')
    status = models.CharField(max_length=20, default='available')
    capacity = models.PositiveIntegerField(default=6)
    members = models.ManyToManyField(Player, related_name='joined_lobbies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Lobbies'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Game(models.Model):
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    choices = models.JSONField()
    result = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lobby.name


class Message(models.Model):
    author = models.ForeignKey(Player, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

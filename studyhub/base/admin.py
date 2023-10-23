from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import Lobby, Message, Game, Player


class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'players'


class PlayersAdmin(AuthUserAdmin):

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(PlayersAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [PlayerInline]
        return super(PlayersAdmin, self).change_view(*args, **kwargs)


admin.site.unregister(User)

admin.site.register(User, PlayersAdmin)
admin.site.register(Lobby)
admin.site.register(Game)
admin.site.register(Message)

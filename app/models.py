# Create your models here.
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    room_name = models.CharField(max_length=50)
    game_status = models.CharField(max_length=50, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def as_json(self):
        return dict(
            id=self.id,
            game_status=self.game_status,
            room_name=self.room_name,
            users=[{'id': u.user.id, 'username': u.user.username, 'followers': u.followers, 'stories': u.stories} for u in self.game_players.all()]
        )


class GamePlayer(models.Model):
    followers = models.IntegerField(default=0)
    stories = models.IntegerField(default=3)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    started = models.BooleanField(default=False)
    game = models.ForeignKey(Game, related_name="game_players", on_delete=models.CASCADE)


class Message(models.Model):
    game = models.ForeignKey(Game, related_name="messages", on_delete=models.CASCADE)
    game_player = models.ForeignKey(GamePlayer, related_name="messages", on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, default=None)

    def as_json(self):
        return dict(
            id=self.id,
            message=self.message,
            message_type=self.message_type,
            created_at=json.dumps(self.created_at, cls=DjangoJSONEncoder),
            game={'id': self.game.id, 'room_name': self.game.room_name},
            user={'id': self.game_player.user.id, 'username': self.game_player.user.username},
        )

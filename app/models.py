# Create your models here.
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import User


class GamePlayer(models.Model):
    followers = models.IntegerField(default=0)
    stories = models.IntegerField(default=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.BooleanField(default=False)


class Game(models.Model):
    room_name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    game_players = models.ManyToManyField(GamePlayer)
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


class Message(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, default=None)

    def as_json(self):
        return dict(
            id=self.id,
            message=self.message,
            message_type=self.message_type,
            created_at=json.dumps(self.created_at, cls=DjangoJSONEncoder),
            game={'id': self.game.id, 'username': self.game.room_name},
            user={'id': self.user.id, 'username': self.user.username},
        )

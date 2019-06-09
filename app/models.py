# Create your models here.
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    room_name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    game_status = models.CharField(max_length=50, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def as_json(self):
        return dict(
            id=self.id,
            game_status=self.game_status,
            room_name=self.room_name,
            users=[{'id': u.id, 'username': u.username} for u in self.users.all()]
        )


class Message(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            id=self.id,
            message=self.message,
            created_at=self.created_at,
            game={'id': self.game.id, 'username': self.game.room_name},
            user={'id': self.user.id, 'username': self.user.username},
        )

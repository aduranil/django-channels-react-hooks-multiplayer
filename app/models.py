# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    room_name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    game_status = models.CharField(max_length=50, default="active")

    def as_json(self):
        return dict(
            id=self.id,
            game_status=self.game_status,
            room_name=self.room_name)

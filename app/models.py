# Create your models here.
import json
import random
from collections import defaultdict

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import User

POST_SELFIE = "post_selfie"
POST_GROUP_SELFIE = "post_group_selfie"
POST_STORY = "post_story"
GO_LIVE = "go_live"
LEAVE_COMMENT = "leave_comment"
DONT_POST = "dont_post"
NO_MOVE = "no_move"
GO_LIVE_DAMAGE = "go_live_damage"
LEAVE_COMMENT_SELF_POINTS = "leave_comment_self_points"
LEAVE_COMMENT_NO_MOVE = "leave_comment_no_move"
LEAVE_COMMENT_GROUP_SELFIE = "leave_comment_group_selfie"

POINTS = dict(
    [
        (POST_SELFIE, 10),
        (POST_GROUP_SELFIE, 20),
        (POST_STORY, 10),
        (GO_LIVE, 20),
        (LEAVE_COMMENT_SELF_POINTS, 0),
        (LEAVE_COMMENT, -5),
        (LEAVE_COMMENT_NO_MOVE, -10),
        (LEAVE_COMMENT_GROUP_SELFIE, -15),
        (DONT_POST, 0),
        (NO_MOVE, -5),
        (GO_LIVE_DAMAGE, -15),
    ]
)


class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects"""

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Game(models.Model):
    room_name = models.CharField(max_length=50)
    game_status = models.CharField(max_length=50, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    round_started = models.BooleanField(default=False)
    is_joinable = models.BooleanField(default=True)

    def as_json(self):
        return dict(
            id=self.id,
            game_status=self.game_status,
            is_joinable=self.is_joinable,
            room_name=self.room_name,
            round_started=self.round_started,
            users=[u.as_json() for u in self.game_players.all()],
            messages=[
                m.as_json()
                for m in self.messages.all()
                .exclude(message_type="round_recap")
                .order_by("created_at")
            ],
            round_history=[
                m.as_json()
                for m in self.messages.all()
                .filter(message_type="round_recap")
                .order_by("created_at")
            ],
            current_round=[r.as_json() for r in self.rounds.all().filter(started=True)],
        )

    def update_player_status(self, player_points):
        winners = []
        for player in self.game.game_players.all():
            points = player_points[player.id]
            updated_points = points + player.followers

            # the floor is zero
            if updated_points <= 0:
                player.loser = True
            else:
                winners.append(player)
            player.followers = updated_points
            player.save()
        return winners

    def can_start_game(self):
        """See if the round can be started. Requires at least 3 players and
        that all players in the room have started"""

        if self.game_players.all().count() < 3:
            self.round_started = False
            self.save()
            return False

        for player in self.game_players.all():
            if player.started is False:
                return False
        self.round_started = True
        self.is_joinable = False  # game is not joinable if the round started
        self.save()
        return True

    def check_joinability(self):
        if self.game_players.all().count() == 6:
            self.is_joinable = False
        elif self.round_started is True:
            self.is_joinable = False
        else:
            self.is_joinable = True
        self.save()

    def set_players_as_not_having_started(self):
        for player in self.game_players.all():
            player.started = False
            player.save()


class GamePlayer(models.Model):
    followers = models.IntegerField(default=100)
    selfies = models.IntegerField(default=3)  # equivalent to licking a lolly
    go_live = models.IntegerField(default=2)  # equivalent to tattle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    loser = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        related_name="game_players",
        on_delete=models.CASCADE,
        primary_key=False,
        default="",
    )
    started = models.BooleanField(default=False)
    game = models.ForeignKey(
        Game, related_name="game_players", on_delete=models.CASCADE
    )
    winner = models.BooleanField(default=False)
    objects = GetOrNoneManager()

    def as_json(self):
        return dict(
            id=self.id,
            winner=self.winner,
            followers=self.followers,
            selfies=self.selfies,
            loser=self.loser,
            go_live=self.go_live,
            username=self.user.username,
            started=self.started,
        )


class Message(models.Model):
    game = models.ForeignKey(Game, related_name="messages", on_delete=models.CASCADE)
    username = models.CharField(max_length=200, default=None)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, default=None)

    def as_json(self):
        return dict(
            id=self.id,
            message=self.message,
            message_type=self.message_type,
            created_at=json.dumps(self.created_at, cls=DjangoJSONEncoder),
            username=self.username,
        )


class Round(models.Model):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    def as_json(self):
        return dict(
            id=self.id,
            started=self.started,
            moves=[m.as_json() for m in self.moves.all()],
        )

    def no_one_moved(self):
        "if no one moved, we want to end the game"
        for move in self.moves.all():
            if move.action_type != "no_move":
                return False
        return True

    def everyone_moved(self):
        "use this function to know if we need to update the clock"
        if self.moves.all().count() == self.game.game_players.all().count():
            return True
        return False

    def update_user_message(self, id, action_type, points, extra=None):
        gp = GamePlayer.objects.get(id=id)
        msg = Message.objects.filter(
            game=self.game, message_type="round_recap", username=gp.user.username
        ).last()
        msg.message = self.generate_new_message(
            action_type, points, gp.user.username, extra
        )
        msg.save()

class Move(models.Model):
    POST_SELFIE = "post_selfie"
    POST_GROUP_SELFIE = "post_group_selfie"
    POST_STORY = "post_story"
    GO_LIVE = "go_live"
    LEAVE_COMMENT = "leave_comment"
    DONT_POST = "dont_post"
    NO_MOVE = "no_move"

    ACTION_TYPES = (
        (POST_SELFIE, "Post a selfie"),
        (POST_GROUP_SELFIE, "Post group selfie"),
        (POST_STORY, "Post a story"),
        (GO_LIVE, "Go live"),
        (LEAVE_COMMENT, "Leave a comment"),
        (DONT_POST, "Don't post"),
        (NO_MOVE, "No move"),
    )

    round = models.ForeignKey(Round, related_name="moves", on_delete=models.CASCADE)
    action_type = models.CharField(
        max_length=200, choices=ACTION_TYPES, default=DONT_POST
    )
    player = models.ForeignKey(
        GamePlayer, related_name="game_player", on_delete=models.CASCADE
    )
    victim = models.ForeignKey(
        GamePlayer,
        related_name="victim",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GetOrNoneManager()

    def as_json(self):
        return dict(
            id=self.id,
            action_type=self.action_type,
            player=self.player.as_json() if self.player else None,
            victim=self.victim.as_json() if self.victim else None,
        )

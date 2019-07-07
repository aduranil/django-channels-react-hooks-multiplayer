# Create your models here.
import json
from collections import defaultdict

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import User


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
            messages=[m.as_json() for m in self.messages.all().order_by('created_at')]
        )

    def can_start_game(self):
        """See if the round can be started. Requires at least 3 players and
        that all players in the room have started"""

        if self.game_players.all().count() <= 2:
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
            self.save()
        elif self.round_started is True:
            self.is_joinable = False
            self.save()
        else:
            self.is_joinable = True
            self.save()


class GamePlayer(models.Model):
    followers = models.IntegerField(default=0)
    stories = models.IntegerField(default=3)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    started = models.BooleanField(default=False)
    game = models.ForeignKey(
        Game,
        related_name="game_players",
        on_delete=models.CASCADE,
    )

    def as_json(self):
        return dict(
            followers=self.followers,
            stories=self.stories,
            username=self.user.username,
            started=self.started,
        )


class Message(models.Model):
    game = models.ForeignKey(
        Game,
        related_name="messages",
        on_delete=models.CASCADE,
    )
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

    def as_json(self):
        return dict(id=self.id, started=self.started)

    def tabulate_round(self):
        # TODO come up with a way to "resolve" a player's actions at a point
        POST_SELFIE = "post_selfie"
        POST_GROUP_SELFIE = "post_group_selfie"
        POST_STORY = "post_story"
        GO_LIVE = "go_live"
        LEAVE_COMMENT = "leave_comment"
        DONT_POST = "dont_post"
        NO_MOVE = "no_move"
        GO_LIVE_DAMAGE = "go_live_damage"
        MEAN_COMMENT_MULTIPLIER = 2
        POINTS = dict([
            (POST_SELFIE, 10),
            (POST_GROUP_SELFIE, 0),
            (POST_STORY, 10),
            (GO_LIVE, 20),
            (LEAVE_COMMENT, -5),
            (DONT_POST, 0),
            (NO_MOVE, -5)
            (GO_LIVE_DAMAGE, -15)]
        )

        # the list has the id of the player who performed that move
        PLAYER_MOVES = dict([
            (POST_SELFIE, []),
            (POST_GROUP_SELFIE, []),
            (POST_STORY, []),
            (GO_LIVE, []),
            (LEAVE_COMMENT, []),
            (DONT_POST, []),
            (NO_MOVE, [])]
        )
        # see which players completed a move during a round
        PLAYERS_WHO_MOVED = []

        # keep a running list of victims during the round
        VICTIMS = defaultdict(lambda: 0)

        # initialize an empty dict of player points to keep track of
        PLAYER_POINTS = defaultdict(lambda: 0)

        # populate what each player did and how many of each type there are
        for move in self.moves.all():
            # TODO refactor this into a switch statement
            if move.action_type == move.POST_SELFIE:
                PLAYER_MOVES[POST_SELFIE].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
            elif move.action_type == move.POST_GROUP_SELFIE:
                PLAYER_MOVES[POST_GROUP_SELFIE].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
            elif move.action_type == move.POST_STORY:
                PLAYER_MOVES[POST_STORY].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
            elif move.action_type == move.GO_LIVE:
                PLAYER_MOVES[GO_LIVE].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
            elif move.action_type == move.LEAVE_COMMENT:
                PLAYER_MOVES[LEAVE_COMMENT].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                VICTIMS[move.victim.user.id] += 1
            elif move.action_type == move.DONT_POST:
                PLAYER_MOVES[DONT_POST].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)

        # see if any of the players didnt move and add a no_move action
        for player in self.game.game_players.all():
            if player.user.id not in PLAYERS_WHO_MOVED:
                PLAYER_MOVES[NO_MOVE].append(player.user.id)
                Move.objects.create(
                    round=self,
                    action_type=NO_MOVE,
                    player=player,
                )

        # TODO convert a group selfie into a regular selfie if there's just 1

        # calculate the points for go live
        if len(PLAYER_MOVES[GO_LIVE]) == 1:
            # if just one player went live, they get 20 points
            PLAYER_POINTS[PLAYER_MOVES[GO_LIVE][0]] = POINTS[GO_LIVE]
            # everyone loses 15 followers who posted a story or selfie
            for user in PLAYER_MOVES[POST_STORY]:
                PLAYER_POINTS[user] += POINTS[GO_LIVE_DAMAGE]
            for user in PLAYER_MOVES[POST_SELFIE]:
                PLAYER_POINTS[user] += POINTS[GO_LIVE_DAMAGE]
        elif len(PLAYER_MOVES[GO_LIVE]) > 1:
            # if more than one player went live they all lose 20 points
            for user in PLAYER_MOVES[GO_LIVE]:
                PLAYER_POINTS[user] -= POINTS[GO_LIVE]


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
    action_type = models.CharField(max_length=200, choices=ACTION_TYPES, default=DONT_POST)
    player = models.ForeignKey(GamePlayer, related_name="game_player", on_delete=models.CASCADE)
    victim = models.ForeignKey(GamePlayer, related_name="victim", blank=True, null=True, on_delete=models.CASCADE)

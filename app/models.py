# Create your models here.
import json
import random
from collections import defaultdict

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import User


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
            messages=[m.as_json() for m in self.messages.all().exclude(message_type="round_recap").order_by("created_at")],
            round_history=[m.as_json() for m in self.messages.all().filter(message_type="round_recap").order_by("created_at")],
            current_round=[r.as_json() for r in self.rounds.all().filter(started=True)],
        )

    def can_start_game(self):
        """See if the round can be started. Requires at least 3 players and
        that all players in the room have started"""

        if self.game_players.all().count() <= 0:
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
    followers = models.IntegerField(default=0)
    stories = models.IntegerField(default=3)
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
    objects = GetOrNoneManager()

    def as_json(self):
        return dict(
            id=self.user.id,
            followers=self.followers,
            stories=self.stories,
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

    objects = GetOrNoneManager()

    def as_json(self):
        return dict(
            id=self.id,
            started=self.started,
            moves=[m.as_json() for m in self.moves.all()],
        )

    def generate_message(
        self, action_type, username, points, updated_points, player_moves, id
    ):
        # player_moves: {'post_selfie': [2], 'post_group_selfie': [], 'post_story': [], 'go_live': [], 'leave_comment': [], 'dont_post': [], 'no_move': []}
        message = "{} did {} and got {} points".format(username, action_type, points)
        if id in player_moves["go_live"]:
            message = "{} went live and got {} points, and now has {}".format(
                username, points, updated_points
            )
            if len(player_moves["go_live"]) > 1:
                message = "{} went live while other girls also went live. what a dummy! She lost {} points and now has {} points".format(
                    username, points, updated_points
                )
        if id in player_moves["dont_post"]:
            message = "{} didn't post and lost {} points. i dont know why since she had nothing better to do.".format(username, points)
        if id in player_moves["post_selfie"]:
            message1 = "{} posted a selfie. how original. she gained {} points".format(
                username, points
            )
            message2 = "{} posted a selfie. cool i guess. she now has {} points".format(username, updated_points)
            message3 = "{} delighted her followers with a beautiful selfie and gained {}".format(username, points)
            message = random.choice([message1, message2, message3])
            if len(player_moves["go_live"]) == 1:
                message = "{} lost {} points because she posted a selfie while another girl was going live!".format(username, points)
        Message.objects.create(message=message, message_type="round_recap", username=username, game=self.game)

    def no_one_moved(self):
        "if no one moved, we want to end the game"
        for move in self.moves.all():
            if move.action_type != "no_move":
                return False
        return True

    def tabulate_round(self):
        POST_SELFIE = "post_selfie"
        POST_GROUP_SELFIE = "post_group_selfie"
        POST_STORY = "post_story"
        GO_LIVE = "go_live"
        LEAVE_COMMENT = "leave_comment"
        DONT_POST = "dont_post"
        NO_MOVE = "no_move"
        GO_LIVE_DAMAGE = "go_live_damage"
        LEAVE_COMMENT_NO_MOVE = "leave_comment_no_move"
        LEAVE_COMMENT_GROUP_SELFIE = "leave_comment_group_selfie"

        POINTS = dict(
            [
                (POST_SELFIE, 10),
                (POST_GROUP_SELFIE, 20),
                (POST_STORY, 10),
                (GO_LIVE, 20),
                (LEAVE_COMMENT, -5),
                (LEAVE_COMMENT_NO_MOVE, -10),
                (LEAVE_COMMENT_GROUP_SELFIE, -15),
                (DONT_POST, 0),
                (NO_MOVE, -5),
                (GO_LIVE_DAMAGE, -15),
            ]
        )

        # the list has the id of the player who performed that move
        PLAYER_MOVES = dict(
            [
                (POST_SELFIE, []),
                (POST_GROUP_SELFIE, []),
                (POST_STORY, []),
                (GO_LIVE, []),
                (LEAVE_COMMENT, []),
                (DONT_POST, []),
                (NO_MOVE, []),
            ]
        )
        # see which players completed a move during a round
        PLAYERS_WHO_MOVED = []

        # keep a running list of victims during the round
        VICTIMS = defaultdict(lambda: 0)

        # initialize an empty dict of player points to keep track of
        PLAYER_POINTS = defaultdict(lambda: 0)

        # populate what each player did and initial points for them
        for move in self.moves.all():
            # TODO refactor this into a switch statement
            if move.action_type == move.POST_SELFIE:
                PLAYER_MOVES[POST_SELFIE].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                # dont update these points until the end
            elif move.action_type == move.POST_GROUP_SELFIE:
                PLAYER_MOVES[POST_GROUP_SELFIE].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                PLAYER_POINTS[move.player.user.id] = POINTS[POST_GROUP_SELFIE]
            elif move.action_type == move.POST_STORY:
                PLAYER_MOVES[POST_STORY].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                PLAYER_POINTS[move.player.user.id] = POINTS[POST_STORY]

                # decrement the number of stories the player has
                game_player = GamePlayer.objects.get(user_id=move.player.user_id, game=self.game)
                game_player.stories = game_player.stories - 1
                game_player.save()
            elif move.action_type == move.GO_LIVE:
                PLAYER_MOVES[GO_LIVE].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                PLAYER_POINTS[move.player.user.id] = POINTS[GO_LIVE]
            elif move.action_type == move.LEAVE_COMMENT:
                PLAYER_MOVES[LEAVE_COMMENT].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                VICTIMS[move.victim.user.id] += 1
                PLAYER_POINTS[move.player.user.id] = POINTS[LEAVE_COMMENT]
            elif move.action_type == move.DONT_POST:
                PLAYER_MOVES[DONT_POST].append(move.player.user.id)
                PLAYERS_WHO_MOVED.append(move.player.user.id)
                PLAYER_POINTS[move.player.user.id] = POINTS[DONT_POST]

        # see if any of the players didnt move and add a no_move action
        for player in self.game.game_players.all():
            if player.user.id not in PLAYERS_WHO_MOVED:
                PLAYER_MOVES[NO_MOVE].append(player.user.id)
                PLAYER_POINTS[player.user.id] = POINTS[NO_MOVE]
                Move.objects.create(round=self, action_type=NO_MOVE, player=player)

        # convert a group selfie into a regular selfie if there's just 1
        if len(PLAYER_MOVES[POST_GROUP_SELFIE]) == 1:
            # update that players points to be the selfie points
            PLAYER_POINTS[PLAYER_MOVES[POST_GROUP_SELFIE][0]] = POINTS[POST_SELFIE]
            # add them to the post_selfie array
            PLAYER_MOVES[POST_SELFIE].append(PLAYER_MOVES[POST_GROUP_SELFIE][0])
            # update the post_group_selfie array
            PLAYER_MOVES[POST_GROUP_SELFIE] = []

        # calculate the points for go live
        if len(PLAYER_MOVES[GO_LIVE]) == 1:

            # delete the user from the array now that their action is resolved
            del PLAYER_MOVES[GO_LIVE][0]

            # everyone loses 15 followers who posted a story
            for user in PLAYER_MOVES[POST_STORY]:
                # UPDATE their points
                PLAYER_POINTS[user] = POINTS[GO_LIVE_DAMAGE]

            # everyone loses 15 followers who posted a selfie
            for user in PLAYER_MOVES[POST_SELFIE]:
                # add points to existing total of 0
                PLAYER_POINTS[user] += POINTS[GO_LIVE_DAMAGE]
        elif len(PLAYER_MOVES[GO_LIVE]) > 1:
            # if more than one player went live they all lose 20 points
            for user in PLAYER_MOVES[GO_LIVE]:
                # UPDATE their points
                PLAYER_POINTS[user] = POINTS[GO_LIVE]

        # calculate the points lost by any victims
        for v in VICTIMS:
            if v in PLAYER_MOVES[POST_SELFIE]:
                # VICTIMS[v] is how many people did the victimizing action
                # POINTS[LEAVE_COMMENT] is -5
                # Don't update points, subtract from existing points
                PLAYER_POINTS[v] += POINTS[LEAVE_COMMENT] * VICTIMS[v]
            if v in PLAYER_MOVES[NO_MOVE]:
                # POINTS[LEAVE_COMMENT_NO_MOVE] is -10
                # UPDATE their points
                PLAYER_POINTS[v] = POINTS[LEAVE_COMMENT_NO_MOVE] * VICTIMS[v]
            if v in PLAYER_MOVES[POST_GROUP_SELFIE]:
                # POINTS[LEAVE_COMMENT_GROUP_SELFIE] is -15
                # UPDATE their points
                PLAYER_POINTS[v] = POINTS[LEAVE_COMMENT_GROUP_SELFIE] * VICTIMS[v]

        # finally tabulate the post_selfies move
        for user in PLAYER_MOVES[POST_SELFIE]:
            if PLAYER_POINTS[user] == 0:
                PLAYER_POINTS[user] = POINTS[POST_SELFIE]

        return [PLAYER_POINTS, PLAYER_MOVES]


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

    def as_json(self):
        return dict(
            id=self.id,
            action_type=self.action_type,
            player=self.player.as_json() if self.player else None,
            victim=self.victim.as_json() if self.victim else None,
        )

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
            id=self.id,
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

    def generate_new_message(self, action_type, followers, username, extra=None):
        message = "{} did {} and got {} followers".format(
            username, action_type, followers
        )
        if action_type == "go_live":  # go_live gets deleted out of player_moves
            message = "{} went live and got {} followers. but for some reason she just played old town road on repeat the whole time".format(
                username, followers
            )
        elif action_type == "dont_post":
            message1 = "{} didn't post and lost {} followers. i dont know why since she had nothing better to do".format(
                username, followers
            )
            message2 = "{} didn't have time to post for some reason. doesn't she know the internet is more important than IRL? she lost {} followers".format(
                username, followers
            )
            message = random.choice([message1, message2])
        elif action_type == "no_move":
            message = "{} was so lazy that she forgot to move. she lost {} followers".format(
                username, followers
            )
        elif action_type == "post_selfie":
            message1 = "{} posted a selfie. how original. she gained {} followers".format(
                username, followers
            )
            message2 = "{} posted a selfie. cool i guess. she got {} followers".format(
                username, followers
            )
            message3 = "{} delighted her followers with a beautiful selfie and gained {} followers".format(
                username, followers
            )
            message = random.choice([message1, message2, message3])
        elif action_type == "post_group_selfie":
            message1 = "{} took a group selfie with some other girls! but are they really friends? the extra popularity gained her {} followers".format(
                username, followers
            )
            message2 = "{} somehow finagled her way into being part of a group selfie. the girls didn't care but she leeched off {} followers anyway".format(
                username, followers
            )
            message = random.choice([message1, message2])
        elif action_type == "post_story":
            message1 = "{} posted a story for {} followers. i hope she got some views".format(
                username, followers
            )
            message2 = "{} posted a story, like we really care what she's up to. she got {} followers for effort though".format(
                username, followers
            )
            message = random.choice([message1, message2])
        elif action_type == "leave_comment":
            message = "{} decided to be petty and left a mean comment, ruining {}'s self esteem".format(
                username, extra
            )
        elif action_type == "one_group_selfie":
            message = "{} tried to be part of a group selfie but no one wanted to join her. so its just her and the sad {} followers she gained".format(
                username, followers
            )
        elif action_type == "go_live_damage":
            message = "{} tried to get attention but {} was live, capturing her followers attention. {} lost {} followers".format(
                username, extra, username, followers
            )
        elif action_type == "many_went_live":
            message = "{} went live at the same time as other girls! how dumb was that? she lost {} followers".format(username, followers)
        elif action_type == "selfie_victim":
            message = "{} got teased relentlessly for her ugly selfie. {} girls teased her. how cruel! she lost {} followers this round".format(
                username, extra, followers
            )
        elif action_type == "no_move_victim":
            message = "{} didnt do anythng, but she still got flamed and lost {} followers".format(
                username, followers
            )
        return message

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

    def tabulate_round(self):

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

        # group_selfie message
        # populate what each player did and initial points for them
        for move in self.moves.all():
            if move.action_type == move.POST_SELFIE:
                PLAYER_MOVES[POST_SELFIE].append(move.player.id)
                PLAYERS_WHO_MOVED.append(move.player.id)
                message = self.generate_new_message(
                    move.POST_SELFIE, POINTS[POST_SELFIE], move.player.user.username
                )
                # dont update these points until the end
            elif move.action_type == move.POST_GROUP_SELFIE:
                PLAYER_MOVES[POST_GROUP_SELFIE].append(move.player.id)
                PLAYERS_WHO_MOVED.append(move.player.id)
                message = self.generate_new_message(
                    move.POST_GROUP_SELFIE,
                    POINTS[POST_GROUP_SELFIE],
                    move.player.user.username,
                )
            elif move.action_type == move.POST_STORY:
                PLAYER_MOVES[POST_STORY].append(move.player.id)
                PLAYERS_WHO_MOVED.append(move.player.id)
                PLAYER_POINTS[move.player.id] = POINTS[POST_STORY]
                message = self.generate_new_message(
                    move.POST_STORY, POINTS[POST_STORY], move.player.user.username
                )
                # decrement the number of stories the player has
                game_player = GamePlayer.objects.get(
                    user_id=move.player.user_id, game=self.game
                )
                game_player.stories = game_player.stories - 1
                game_player.save()
            elif move.action_type == move.GO_LIVE:
                PLAYER_MOVES[GO_LIVE].append(move.player.id)
                PLAYERS_WHO_MOVED.append(move.player.id)
                PLAYER_POINTS[move.player.id] = POINTS[GO_LIVE]
                message = self.generate_new_message(
                    move.GO_LIVE, POINTS[GO_LIVE], move.player.user.username
                )
            elif move.action_type == move.LEAVE_COMMENT:
                PLAYER_MOVES[LEAVE_COMMENT].append(move.player.id)
                PLAYERS_WHO_MOVED.append(move.player.id)
                message = self.generate_new_message(
                    move.LEAVE_COMMENT,
                    POINTS[LEAVE_COMMENT],
                    move.player.user.username,
                    move.victim.user.username,
                )
                VICTIMS[move.victim.id] += 1
                PLAYER_POINTS[move.player.id] = 0
            elif move.action_type == move.DONT_POST:
                PLAYER_MOVES[DONT_POST].append(move.player.id)
                PLAYERS_WHO_MOVED.append(move.player.id)
                PLAYER_POINTS[move.player.id] = POINTS[DONT_POST]
                message = self.generate_new_message(
                    move.DONT_POST, POINTS[DONT_POST], move.player.user.username
                )
            Message.objects.create(
                message=message,
                message_type="round_recap",
                username=move.player.user.username,
                game=self.game,
            )

        # see if any of the players didnt move and add a no_move action
        for player in self.game.game_players.all():
            if player.id not in PLAYERS_WHO_MOVED:
                PLAYER_MOVES[NO_MOVE].append(player.id)
                PLAYER_POINTS[player.id] = POINTS[NO_MOVE]
                Move.objects.create(round=self, action_type=NO_MOVE, player=player)
                message = self.generate_new_message(
                    NO_MOVE, -POINTS[NO_MOVE], player.user.username
                )
                Message.objects.create(
                    message=message,
                    message_type="round_recap",
                    username=player.user.username,
                    game=self.game,
                )
        # convert a group selfie into a regular selfie if there's just 1
        if len(PLAYER_MOVES[POST_GROUP_SELFIE]) == 1:
            # we need to update the message now
            self.update_user_message(
                PLAYER_MOVES[POST_GROUP_SELFIE][0],
                "one_group_selfie",
                POINTS[POST_SELFIE],
            )
            # update that players points to be the selfie points
            PLAYER_POINTS[PLAYER_MOVES[POST_GROUP_SELFIE][0]] = 0
            # add them to the post_selfie array
            PLAYER_MOVES[POST_SELFIE].append(PLAYER_MOVES[POST_GROUP_SELFIE][0])
            # update the post_group_selfie array
            PLAYER_MOVES[POST_GROUP_SELFIE] = []

        # calculate the points for go live
        if len(PLAYER_MOVES[GO_LIVE]) == 1:
            # delete the user from the array now that their action is resolved
            girl_who_went_live = GamePlayer.objects.get(id=PLAYER_MOVES[GO_LIVE][0])
            del PLAYER_MOVES[GO_LIVE][0]

            # everyone loses 15 followers who posted a story
            for user in PLAYER_MOVES[POST_STORY]:
                # UPDATE their points
                PLAYER_POINTS[user] = POINTS[GO_LIVE_DAMAGE]
                self.update_user_message(
                    id=user,
                    action_type="go_live_damage",
                    points=-PLAYER_POINTS[user],
                    extra=girl_who_went_live.user.username,
                )

            # everyone loses 15 followers who posted a selfie
            for user in PLAYER_MOVES[POST_SELFIE]:
                # UPDATE their points
                PLAYER_POINTS[user] += POINTS[GO_LIVE_DAMAGE]
                self.update_user_message(
                    user,
                    "go_live_damage",
                    -PLAYER_POINTS[user],
                    girl_who_went_live.user.username,
                )
            # everyone loses 15 followers who posted a group selfie
            for user in PLAYER_MOVES[POST_GROUP_SELFIE]:
                # add points to existing total of 0
                PLAYER_POINTS[user] += POINTS[GO_LIVE_DAMAGE]
                self.update_user_message(
                    user,
                    "go_live_damage",
                    -PLAYER_POINTS[user],
                    girl_who_went_live.user.username,
                )
        elif len(PLAYER_MOVES[GO_LIVE]) > 1:
            # if more than one player went live they all lose 20 points
            for user in PLAYER_MOVES[GO_LIVE]:
                # UPDATE their points
                PLAYER_POINTS[user] = -POINTS[GO_LIVE]
                self.update_user_message(user, "many_went_live", -PLAYER_POINTS[user])

        # calculate the points lost by any victims
        for v in VICTIMS:
            if v in PLAYER_MOVES[POST_SELFIE]:
                # VICTIMS[v] is how many people did the victimizing action
                # POINTS[LEAVE_COMMENT] is -5
                # Don't update points, subtract from existing points
                PLAYER_POINTS[v] += POINTS[LEAVE_COMMENT] * VICTIMS[v]
                self.update_user_message(
                    v, "selfie_victim", -PLAYER_POINTS[v], VICTIMS[v]
                )

            if v in PLAYER_MOVES[NO_MOVE]:
                # POINTS[LEAVE_COMMENT_NO_MOVE] is -10
                # UPDATE their points
                PLAYER_POINTS[v] = POINTS[LEAVE_COMMENT_NO_MOVE] * VICTIMS[v]
                self.update_user_message(
                    v, "no_move_victim", -PLAYER_POINTS[v], VICTIMS[v]
                )

            if v in PLAYER_MOVES[POST_GROUP_SELFIE]:
                # POINTS[LEAVE_COMMENT_GROUP_SELFIE] is -15
                # UPDATE their points
                PLAYER_POINTS[v] += POINTS[LEAVE_COMMENT_GROUP_SELFIE] * VICTIMS[v]
                self.update_user_message(
                    v, "selfie_victim", -PLAYER_POINTS[v], VICTIMS[v]
                )

        # finally tabulate the post_selfies move
        for user in PLAYER_MOVES[POST_SELFIE]:
            if PLAYER_POINTS[user] == 0:
                PLAYER_POINTS[user] = POINTS[POST_SELFIE]
        for user in PLAYER_MOVES[POST_GROUP_SELFIE]:
            if PLAYER_POINTS[user] == 0:
                PLAYER_POINTS[user] = POINTS[POST_GROUP_SELFIE]
        print(PLAYER_POINTS)
        return PLAYER_POINTS


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

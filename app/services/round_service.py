from collections import defaultdict
import random

from app.models import Move, Message
from app.services import message_service

# moves

# they dont lose any points if they don't post when you leave a comment
LEAVE_COMMENT = "leave_comment"  # equivalent to scratch, they lose 10 points.
LEAVE_COMMENT_DM = -10

# only works if two or more people do it. the target loses 20 points for each
# girl that dislikes her.
DISLIKE = "dislike"
DISLIKE_DM = -20

# if you call a girl it interrupts what she's going to do. she can't leave a
# comment, dislike, or go live.
CALL_IPHONE = "call_iphone"


POST_SELFIE = "post_selfie"  # available 3 times per game. you gain back 20 points.
# you are immune to go_live. if someone calls you or leaves a comment you lose 20 points
POST_SELFIE_PTS = 20
POST_SELFIE_DM = -20

# two go live per game. everyone loses 30 points unless two girls go live at
# the same time.
GO_LIVE = "go_live"
GO_LIVE_DM = -30

DONT_POST = "dont_post"  # you cant not post twice in a row. the second time you
# don't post you lose 10 followers if it was for no reason.
DONT_POST_DM = -10

NO_MOVE = "no_move"  # lose 10 points
NO_MOVE_DM = -10


class RoundTabulation(object):
    """tabulate the round"""

    def __init__(self, round):
        # the list has the id of the player who performed that move
        self.player_moves = dict(
            [
                (POST_SELFIE, []),
                (LEAVE_COMMENT, []),
                (CALL_IPHONE, []),
                (DISLIKE, []),
                (GO_LIVE, []),
                (DONT_POST, []),
                (NO_MOVE, []),
            ]
        )
        # see which players completed a move during a round
        self.players_who_moved = []
        # keep a running list of victims during the round
        # victims = { 1: {dislike: 1, call: 2}}
        self.victims = {}
        # initialize an empty dict of player points to keep track of
        self.player_points = defaultdict(lambda: 0)
        self.round = round

    def populate_arrays_with_player_moves(self):
        for move in self.round.moves.all():
            # see if there is more than 1 go_live for later
            self.player_moves[move.action_type].append(move.player.id)
            # determine who moved during the round
            self.players_who_moved.append(move.player.id)
            # initialize a dict with 0 points for everyone
            self.player_points[move.player.id] = 0
            # initialize a victim dict to tally points later
            self.victims[move.player.id] = {
                "dislike": [],
                "call_iphone": [],
                "leave_comment": [],
            }

        # see if any of the players didnt move and add a no_move action
        # possible because we already determined which players moved
        self.determine_if_player_didnt_move()

        for move in self.round.moves.all():
            # now that victims are initialized, see who was disliked, called, etc
            if move.victim:
                self.victims[move.victim.id][move.action_type].append(
                    move.player.user.username
                )
        return self.victims

    def determine_if_player_didnt_move(self):
        for player in self.round.game.game_players.all():
            if player.id not in self.players_who_moved:
                self.player_moves[NO_MOVE].append(player.id)
                self.player_points[player.id] = 0
                self.victims[player.id] = {
                    "dislike": [],
                    "call_iphone": [],
                    "leave_comment": [],
                }
                Move.objects.create(
                    round=self.round, action_type=NO_MOVE, player=player, victim=None
                )

    def tabulate_go_live(self, move):
        points = 0
        calls = self.victims[move.player.id][CALL_IPHONE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        dislikes = self.victims[move.player.id][DISLIKE]
        move.player.go_live = move.player.go_live - 1
        move.player.save()
        go_live_success = True
        called = False
        # see if they're still in the player moves array cause they could have been called
        if move.player.id in self.player_moves[GO_LIVE]:
            if len(self.player_moves[GO_LIVE]) > 1:
                points += GO_LIVE_DM
                go_live_success = False
        else:
            # if they're not in the player moves array
            if len(self.player_moves[GO_LIVE]) == 1:
                points += GO_LIVE_DM
                called = True
                go_live_success = False

        # determine any damage from any mean comments
        points += len(comments) * LEAVE_COMMENT_DM
        # determine any damage from any dislikes
        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM

        self.player_points[move.player.id] = points
        message_service.go_live_message(move, points, go_live_success, called)

    def tabulate_dont_post(self, move):
        points = 0
        dislikes = self.victims[move.player.id][DISLIKE]
        calls = self.victims[move.player.id][CALL_IPHONE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        go_live = self.player_moves[GO_LIVE]

        # not posting doesnt protect you against dislikes
        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM

        no_post_last_round = False
        moves = Move.objects.all().filter(player=move.player).order_by("-created_at")
        if len(moves) >= 2 and moves[1].action_type == DONT_POST:
            no_post_last_round = True

        if no_post_last_round:
            if not (
                len(dislikes) > 1
                or len(calls) >= 1
                or len(comments) >= 1
                or len(go_live) == 1
            ):
                points += DONT_POST_DM
            message_service.dont_post_msg(move, repeat=True)
        else:
            message_service.dont_post_msg(move, repeat=False)
        self.player_points[move.player.id] = points

    def tabulate_post_selfie(self, move):
        points = POST_SELFIE_PTS
        calls = self.victims[move.player.id][CALL_IPHONE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        go_live = self.player_moves[GO_LIVE]
        messages = None

        # decrement selfies left
        move.player.selfies = move.player.selfies - 1
        move.player.save()

        # if someone calls you you don't get to take the selfie
        # and you sustain go live damage
        if len(calls) >= 1:
            points = 0
            if len(go_live) == 1:
                points += GO_LIVE_DM

        # if someone leaves a comment, its double damage
        if len(comments) >= 1:
            messages = message_service.post_selfie_msg(
                move, points, called=False, comments=True
            )
            points = len(comments) * POST_SELFIE_DM

        if not messages:
            message_service.post_selfie_msg(move, points)

        self.player_points[move.player.id] = points

    def tabulate_call_iphone(self, move):
        calls = self.victims[move.player.id][CALL_IPHONE]
        # someone can call the player, which can prevent them from doing something
        if len(calls) >= 1:
            message = "{} tried to call {}, but she was blocked".format(
                move.player.user.username, move.victim.user.username
            )
            Message.objects.create(
                message=message,
                message_type="round_recap",
                username=move.player.user.username,
                game=move.round.game,
            )
            if move.player.user.username in self.victims[move.victim.id][CALL_IPHONE]:
                self.victims[move.victim.id][CALL_IPHONE].remove(
                    move.player.user.username
                )
            # if move.player.user.username in self.victims[move.victim.id][LEAVE_COMMENT]:
            #     self.victims[move.victim.id][LEAVE_COMMENT].remove(move.player.user.username)
            # if move.player.user.username in self.victims[move.victim.id][DISLIKE]:
            #     self.victims[move.victim.id][DISLIKE].remove(move.player.user.username)
        else:
            # otherwise check if they called someone who went live and
            # remove them from the array so later we can see how many points
            victim_move = Move.objects.filter(player=move.victim).latest(                "created_at")
            message_service.iphone_msg(
                move, move.victim.user.username, victim_move.action_type
            )
            if move.victim.id in self.player_moves[GO_LIVE]:
                self.player_moves[GO_LIVE].remove(move.victim.id)

            if move.victim.id in self.player_moves[LEAVE_COMMENT]:
                self.player_moves[LEAVE_COMMENT].remove(move.victim.id)

            if move.victim.id in self.player_moves[DISLIKE]:
                self.player_moves[DISLIKE].remove(move.victim.id)

            for victim in self.victims:
                if move.victim.user.username in self.victims[victim][LEAVE_COMMENT]:
                    self.victims[victim][LEAVE_COMMENT].remove(
                        move.victim.user.username
                    )
                if move.victim.user.username in self.victims[victim][DISLIKE]:
                    self.victims[victim][DISLIKE].remove(move.victim.user.username)
                if move.victim.user.username in self.victims[victim][CALL_IPHONE]:
                    self.victims[victim][CALL_IPHONE].remove(move.victim.user.username)

    def tabulate_call_iphone_again(self, move):
        points = 0
        dislikes = self.victims[move.player.id][DISLIKE]
        go_live = self.player_moves[GO_LIVE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]

        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM

        if len(comments) >= 1:
            points += len(comments) * LEAVE_COMMENT_DM

        if len(go_live) == 1:
            points += GO_LIVE_DM

        self.player_points[move.player.id] = points

    def tabulate_no_move(self, move):
        points = NO_MOVE_DM
        dislikes = self.victims[move.player.id][DISLIKE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        go_live = self.player_moves[GO_LIVE]
        messages = None

        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM
            messages = message_service.no_move_msg(move, comments=True)

        if len(comments) >= 1:
            points += len(comments) * LEAVE_COMMENT_DM
            if not messages:
                messages = message_service.no_move_msg(move, comments=True)

        if len(go_live) == 1:
            points += GO_LIVE_DM

        if not messages:
            message_service.no_move_msg(move)

        self.player_points[move.player.id] = points

    def tabulate_leave_comment(self, move):
        points = 0
        dislikes = self.victims[move.player.id][DISLIKE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        go_live = self.player_moves[GO_LIVE]

        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM

        if len(comments) >= 1:
            points += len(comments) * LEAVE_COMMENT_DM

        if len(go_live) == 1:
            points += GO_LIVE_DM

        # check if the player was grabbed
        grabbed = False
        if move.player.id not in self.player_moves[LEAVE_COMMENT]:
            grabbed = True
            # they werent grabbed from doing the action
        message_service.leave_comment_msg(
            move, move.victim.user.username, grabbed=grabbed
        )

        self.player_points[move.player.id] = points

    def tabulate_dislike(self, move):
        points = 0
        dislikes = self.victims[move.player.id][DISLIKE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        go_live = self.player_moves[GO_LIVE]

        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM

        if len(comments) >= 1:
            points += len(comments) * LEAVE_COMMENT_DM

        if len(go_live) == 1:
            points += GO_LIVE_DM

        # check if the player was grabbed
        grabbed = False
        if move.player.id not in self.player_moves[DISLIKE]:
            grabbed = True

        multiple_dislikes = False
        if len(self.victims[move.victim.id][DISLIKE]) >= 2:
            multiple_dislikes = True

        message_service.dislike_msg(
            move, move.victim.user.username, points, grabbed, multiple_dislikes
        )

        self.player_points[move.player.id] = points

    def tabulate(self):
        self.populate_arrays_with_player_moves()
        for move in self.round.moves.all():
            if move.action_type == CALL_IPHONE:
                self.tabulate_call_iphone(move)

        for move in self.round.moves.all():
            if move.action_type == GO_LIVE:
                self.tabulate_go_live(move)
            elif move.action_type == DONT_POST:
                self.tabulate_dont_post(move)
            elif move.action_type == POST_SELFIE:
                self.tabulate_post_selfie(move)
            elif move.action_type == CALL_IPHONE:
                self.tabulate_call_iphone_again(move)
            elif move.action_type == NO_MOVE:
                self.tabulate_no_move(move)
            elif move.action_type == LEAVE_COMMENT:
                self.tabulate_leave_comment(move)
            elif move.action_type == DISLIKE:
                self.tabulate_dislike(move)
        return self.player_points

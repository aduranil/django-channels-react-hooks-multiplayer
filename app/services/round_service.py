from collections import defaultdict
import random

from app.models import Move
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
        move.player.go_live = move.player.go_live - 1
        move.player.save()
        if len(self.victims[move.player.id][CALL_IPHONE]) >= 1:
            callers = self.victims[move.player.id][CALL_IPHONE]
            message_service.iphone_msg(move, callers)
            # delete them from the GO_LIVE array
            self.player_moves[GO_LIVE].remove(move.player.id)

        # determine any damage from any mean comments
        points += len(self.victims[move.player.id][LEAVE_COMMENT]) * LEAVE_COMMENT_DM
        # determine any damage from any dislikes
        if len(self.victims[move.player.id][DISLIKE]) > 1:
            points += len(self.victims[move.player.id][DISLIKE]) * DISLIKE_DM

        self.player_points[move.player.id] = points

    def tabulate_dont_post(self, move):
        points = 0
        dislikes = self.victims[move.player.id][DISLIKE]
        calls = self.victims[move.player.id][CALL_IPHONE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]
        go_live = self.player_moves[GO_LIVE]

        # not posting doesnt protect you against dislikes
        if len(dislikes) > 1:
            points += len(dislikes) * DISLIKE_DM

        no_post_last_round = Move.objects.get_or_none(id=move.id - 1, action_type=DONT_POST, player=move.player)
        if no_post_last_round:
            if not (len(dislikes) > 1 or len(calls) >= 1 or len(comments) >=1 or len(go_live) == 1):
                points += DONT_POST_DM
            message_service.dont_post_msg(move, repeat=True)
        else:
            message_service.dont_post_msg(move, repeat=False)
        self.player_points[move.player.id] = points

    def tabulate_post_selfie(self, move):
        points = POST_SELFIE_PTS
        calls = self.victims[move.player.id][CALL_IPHONE]
        comments = self.victims[move.player.id][LEAVE_COMMENT]

        # decrement selfies left
        move.player.selfies = move.player.selfies - 1
        move.player.save()

        # if someone calls you you don't get to take the selfie
        if len(calls) >= 1:
            points = 0

        # if someone leaves a comment, its double damage
        if len(comments) >= 1:
            points = len(comments) * POST_SELFIE_DM
        message_service.post_selfie_msg(move.player.user.username)
        self.player_points[move.player.id] = points

    def tabulate(self):
        self.populate_arrays_with_player_moves()
        for move in self.round.moves.all():
            if move.action_type == GO_LIVE:
                self.tabulate_go_live(move)
            elif move.action_type == DONT_POST:
                self.tabulate_dont_post(move)
            elif move.action_type == POST_SELFIE:
                self.tabulate_post_selfie(move)
        return self.player_points

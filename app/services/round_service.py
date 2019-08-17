from collections import defaultdict

from app.models import Move
# moves

# they dont lose any points if they don't post when you leave a comment
LEAVE_COMMENT = "leave_comment" # equivalent to scratch, they lose 10 points.
LEAVE_COMMENT_DM = -10

# only works if two or more people do it. the target loses 20 points for each
# girl that dislikes her.
DISLIKE = "dislike"
DISLIKE_DM = -20

# if you call a girl it interrupts what she's going to do. she can't leave a
# comment, dislike, or go live.
CALL_IPHONE = "call_iphone"


POST_SELFIE = "post_selfie" # available 3 times per game. you gain back 20 points.
# you are immune to go_live. if someone calls you or leaves a comment you lose 20 points
POST_SELFIE_PTS = 20
POST_SELFIE_DM = -20

# two go live per game. everyone loses 30 points unless two girls go live at
# the same time.
GO_LIVE = "go_live"
GO_LIVE_DM = -30

DONT_POST = "dont_post" # you cant not post twice in a row. the second time you
# don't post you lose 10 followers if it was for no reason.
DONT_POST_DM = -10

NO_MOVE = "no_move" # lose 10 points
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
            self.player_moves[move.action_type].append(move.player.id)
            self.players_who_moved.append(move.player.id)
            self.player_points[move.player.id] = 0
            self.victims[move.player.id] = {'dislike': 0, 'call_iphone': 0, 'leave_comment': 0}

        # see if any of the players didnt move and add a no_move action
        self.determine_if_player_didnt_move()

        for move in self.round.moves.all():
            if move.victim:
                self.victims[move.victim.id][move.action_type] += 1

        return self.victims

    def determine_if_player_didnt_move(self):
        for player in self.round.game.game_players.all():
            if player.id not in self.players_who_moved:
                self.player_moves[NO_MOVE].append(player.id)
                self.player_points[player.id] = 0
                self.victims[player.id] = {'dislike': 0, 'call_iphone': 0, 'leave_comment': 0}
                Move.objects.create(round=self.round, action_type=NO_MOVE, player=player)

    def tabulate(self):
        self.populate_arrays_with_player_moves()
        for move in self.round.moves.all():
            points = 0
            if move.action_type == GO_LIVE:
                move.player.go_live = move.player.go_live - 1
                move.save()
                if self.victims[move.victim.id][CALL_IPHONE] >= 1:
                    points = 0
                    self.iphone_msg(move.player.user.username)


    def iphone_msg(self, player):
        message1 = "{} tried to go live, but she was distracted by a phone call!".format(player)
        return [message1]



    def tabulate_round(self):
        # group_selfie message
        # populate what each player did and initial points for them


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

    def generate_new_message(self, action_type, followers, username, extra=None):
        message = "{} did {} and got {} followers".format(
            username, action_type, followers
        )
        if action_type == "go_live":
            message1 = "{} shared her political opinions while going live and got {} followers. chemtrails are real".format(
                username, followers
            )
            message2 = "{} went live and got {} followers, but she just played old town road on repeat the whole time".format(
                username, followers
            )
            message3 = "{} got shady during her go live sesh. she was interesting enough to get {} followers".format(
                username, followers
            )
            message4 = "{} shared photos of her food while going live. her {} new followers seemingly loved it".format(username, followers)
            message = random.choice([message1, message2, message3, message4])
        elif action_type == "dont_post":
            message1 = "{} didn't post and lost {} followers even though she had nothing better to do".format(
                username, followers
            )
            message2 = "{} didn't have time to post. doesn't she know the internet is more important than IRL? she lost {} followers".format(
                username, followers
            )
            message3 = "{} didn't post. was she getting fillers or something?"
            message = random.choice([message1, message2, message3])
        elif action_type == "no_move":
            message1 = "{} was so lazy that she forgot to move. she lost {} followers".format(
                username, followers
            )
            message2 = "{} didn't move this round. honestly, i hate her. so do the {} followers she lost".format(username, followers)
            message3 = "if {} forgets to move again, she's getting cancelled permanently! she lost {} followers".format(username, followers)
            message = random.choice([message1, message2, message3])
        elif action_type == "post_selfie":
            message1 = "{} posted a selfie. how original. she gained {} followers".format(
                username, followers
            )
            message2 = "drumroll please...{} posted a selfie. cool i guess. she got {} followers".format(
                username, followers
            )
            message3 = "{} delighted her followers with a beautiful selfie and gained {} followers".format(
                username, followers
            )
            message4 = "{} showed off a cute new outfit in a classic mirror selfie. her {} new followers loved it!".format(
                username, followers
            )
            message = random.choice([message1, message2, message3, message4])
        elif action_type == "post_group_selfie":
            message1 = "{} took a group selfie with some other girls! but are they really friends? the extra popularity gained her {} followers".format(
                username, followers
            )
            message2 = "{} somehow finagled her way into being part of a group selfie. the girls didn't care but she leeched off {} followers anyway".format(
                username, followers
            )
            message3 = "{} is in a selfie with other people? i guess anything is possible. she now has {} followers".format(username, followers)
            message = random.choice([message1, message2, message3])
        elif action_type == "post_story":
            message1 = "{} posted a story for {} followers. i hope she got some views".format(
                username, followers
            )
            message2 = "{} posted a story, like we really care what she's up to. she got {} followers for effort though".format(
                username, followers
            )
            message3 = "{} used way too many filters on the story she just posted. her {} new followers must not have noticed".format(username, followers)
            message = random.choice([message1, message2, message3])
        elif action_type == "leave_comment":
            message1 = "{} decided to be petty and left a mean comment, ruining {}'s self esteem".format(
                username, extra
            )
            message2 = "{} absolutely destroyed {}'s new selfie. she's a total hater!".format(
                username, extra
            )
            message3 = "{} called {}'s bag cheap and tacky. what a mean comment".format(username, extra)
            message = random.choice([message1, message2, message3])
        elif action_type == "one_group_selfie":
            message1 = "{} tried to be part of a group selfie but no one wanted to join her. so its just her and the sad {} followers she gained".format(
                username, followers
            )
            message2 = "{} posed for a group selfie. alone. pathetic. {} dummies still like it though".format(username, followers)
            message3 = "{} has no friends, which is why her sad group selfie attempt failed. her solo selfie got {} followers".format(username, followers)
            message = random.choice([message1, message2, message3])
        elif action_type == "go_live_damage":
            message = "{} tried to get attention but {} was live, capturing her followers attention. {} lost {} followers".format(
                username, extra, username, followers
            )
        elif action_type == "many_went_live":
            message1 = "{} went live at the same time as other girls! how dumb was that? she lost {} followers".format(username, followers)
            message2 = "{} went live! she timed it poorly though and lost {} followers".format(username, followers)
            message = random.choice([message1, message2, message3])
        elif action_type == "selfie_victim":
            message = "{} got teased relentlessly for her ugly selfie. {} girls teased her. how cruel! she lost {} followers this round".format(
                username, extra, followers
            )
        elif action_type == "no_move_victim":
            message = "{} didnt do anything, but she still got flamed and lost {} followers".format(
                username, followers
            )
        return message

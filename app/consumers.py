""" All of the websocket actions for the game and chat functionalities"""
import json
import time
import threading

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Game, Message, GamePlayer, Round, Move
from app.services.round_service import RoundTabulation


class GameConsumer(WebsocketConsumer):
    """Websocket for inside of the game"""

    def connect(self):
        game_id = self.scope["url_route"]["kwargs"]["id"]
        self.id = game_id
        self.room_group_name = "game_%s" % self.id
        self.game = Game.objects.get(id=game_id)
        self.user = self.scope["user"]
        self.game_player = GamePlayer.objects.get_or_none(
            user=self.user, game=self.game
        )
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self.join_game()

    def disconnect(self, close_code):
        pass

    # GAME MOVE ACTIONS
    def join_game(self):
        if not self.game_player and self.game.is_joinable:
            GamePlayer.objects.create(user=self.user, game=self.game)
            Message.objects.create(
                message="{} joined".format(self.user.username),
                game=self.game,
                username=self.user.username,
                message_type="action",
            )
            self.game.check_joinability()

        self.send_update_game_players()

    def leave_game(self, data=None):
        print("in leave game")
        game_player = GamePlayer.objects.get_or_none(user=self.user, game=self.game)
        if self.game.game_players.all().count() == 0:
            game_player.delete()
            self.game.delete()
        else:
            Message.objects.create(
                message="{} left".format(self.user.username),
                game=self.game,
                username=self.user.username,
                message_type="action",
            )
            game_player.delete()
            self.game.check_joinability()
            self.send_update_game_players()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def new_message(self, data):
        Message.objects.create(
            message=data["message"],
            message_type="user_message",
            game=self.game,
            username=self.user.username,
        )
        self.send_update_game_players()

    def start_round(self, data=None):
        """Checks if the user has opted in to starting the game"""

        game_player = GamePlayer.objects.get(user=self.scope["user"], game=self.game)
        game_player.started = True
        game_player.save()
        self.send_update_game_players()
        if self.game.can_start_game():
            # start the timer in another thread
            Round.objects.create(game=self.game, started=True)
            # pass round so we can set it to false after the time is done
            self.start_round_and_timer()

    def start_round_and_timer(self):
        threading.Thread(target=self.update_timer_data).start()
        self.send_update_game_players()

    def update_timer_data(self):
        """countdown the timer for the game"""
        i = 90
        while i > 0:
            time.sleep(1)
            self.send_time(str(i))
            i -= 1
            try:
                round = Round.objects.get_or_none(game=self.game, started=True)
            except Exception:
                round = Round.objects.filter(game=self.game, started=True).latest(
                    "created_at"
                )
            if round.everyone_moved():
                i = 0
                j = 10
                while j > 0:
                    time.sleep(1)
                    self.send_time(str(j))
                    j -= 1

        # reset timer back to null
        self.send_time(None)
        self.new_round_or_determine_winner()

    def new_round_or_determine_winner(self):
        "determines a winner or loops through again"
        try:
            round = Round.objects.get_or_none(game=self.game, started=True)
        except Exception:
            round = Round.objects.filter(game=self.game, started=True).latest(
                "created_at"
            )
        if round:
            player_points = RoundTabulation(round).tabulate()
            winners = self.game.update_player_status(player_points)

            if round.no_one_moved():
                print("no one moved")
                # the below 4 things can be combined into one reset_game method
                self.game.round_started = False
                self.game.is_joinable = True
                self.game.set_players_as_not_having_started()
                self.game.save()
                round.started = False
                round.save()

                return self.send_update_game_players()

            round.started = False
            round.save()
            Round.objects.create(game=self.game, started=True)
            if len(winners) != 2:
                self.start_round_and_timer()
            else:
                self.game.game_status = "inactive"
                self.game.save()
                for winner in winners:
                    Message.objects.create(
                        message="{} won!".format(winner.user.username),
                        message_type="round_recap",
                        game=self.game,
                        username=winner.user.username,
                    )
                self.send_update_game_players()
                async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name, self.channel_name
                )

    def make_move(self, data):
        user = self.scope["user"]
        try:
            round = Round.objects.get_or_none(game=self.game, started=True)
        except Exception:
            round = Round.objects.filter(game=self.game, started=True).latest(
                "created_at"
            )

        game_player = GamePlayer.objects.get_or_none(user=user, game=self.game)
        try:
            move = Move.objects.get(player=game_player, round=round)
            move.action_type = data["move"]["move"]
            # if in a former move they left a comment but now they want to
            # do something else, a victim is still saved on the Move object
            # update victim to be none in this case
            if data["move"]["move"] is not "leave_comment" and move.victim is not None:
                move.victim = None
            move.save()
        except Exception:
            move = Move.objects.create(
                round=round, action_type=data["move"]["move"], player=game_player
            )
        # save the victim if they are there
        if data["move"]["victim"]:
            victim = GamePlayer.objects.get(id=data["move"]["victim"], game=self.game)
            move.victim = victim
            move.save()

    # ASYNC TO SYNC ACTIONS
    def send_update_game_players(self):
        """sends all game info as a json object when there's an update"""
        game = Game.objects.get(id=self.id)
        game_player = GamePlayer.objects.get_or_none(user=self.scope["user"], game=game)
        current_player = game_player.as_json() if game_player else None
        if current_player:
            self.update_game_players(
                {"type": "update_game_player", "current_player": current_player}
            )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "update_game_players", "game": game.as_json()},
        )

    def send_time(self, time):
        """sends the current time on the clock"""
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "update_timer", "time": time}
        )

    # SEND DATA ACTIONS
    def update_game_players(self, current_player):
        self.send(text_data=json.dumps(current_player))

    def update_timer(self, timedata):
        self.send(text_data=json.dumps(timedata))

    def receive(self, text_data):
        data = json.loads(text_data)

        self.commands[data["command"]](self, data)

    commands = {
        "update_timer": update_timer,
        "LEAVE_GAME": leave_game,
        "NEW_MESSAGE": new_message,
        "START_ROUND": start_round,
        "MAKE_MOVE": make_move,
    }

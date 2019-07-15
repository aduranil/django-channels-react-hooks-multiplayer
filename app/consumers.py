""" All of the websocket actions for the game and chat functionalities"""
import json

from asgiref.sync import async_to_sync
import time
import threading
from channels.generic.websocket import WebsocketConsumer

from .models import Game, Message, GamePlayer, Round, Move


class GameConsumer(WebsocketConsumer):
    """Websocket for inside of the game"""
    def connect(self):
        game_id = self.scope['url_route']['kwargs']['id']
        self.id = game_id
        self.room_group_name = 'game_%s' % self.id
        self.game = Game.objects.get(id=game_id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()
        self.join_game()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # GAME MOVE ACTIONS
    def join_game(self):
        user = self.scope['user']
        game = Game.objects.get(id=self.id)
        if not hasattr(user, 'gameplayer') and game.is_joinable:
            GamePlayer.objects.create(user=user, game=game)
            message = '{} joined'.format(user.username)
            Message.objects.create(
                message=message,
                game=game,
                username=user.username,
                message_type="action"
            )
            game.check_joinability()

        self.send_update_game_players(game)

    def leave_game(self, data):
        user = self.scope['user']

        game_player = GamePlayer.objects.get(user=user)
        # retrieve the updated game
        game = Game.objects.get(id=self.id)
        if game.game_players.all().count() == 1:
            game.delete()
        else:
            message = '{} left'.format(user.username)
            Message.objects.create(
                message=message,
                game=game,
                username=user.username,
                message_type="action",
            )
            game_player.delete()
            game.check_joinability()
            self.send_update_game_players(game)

    def new_message(self, data):
        user = self.scope['user']
        game = Game.objects.get(id=self.id)
        Message.objects.create(
            message=data['message'],
            message_type='user_message',
            game=game,
            username=user.username,
        )
        self.send_update_game_players(game)

    def start_round(self, data):
        """Checks if the user has opted in to starting the game"""
        user = self.scope['user']
        game = Game.objects.get(id=self.id)
        game_player = GamePlayer.objects.get(user=user)
        game_player.started = True
        game_player.save()
        self.send_update_game_players(game)
        if game.can_start_game():
            # start the timer in another thread
            round = Round.objects.create(game=game, started=True)
            # pass round so we can set it to false after the time is done
            threading.Thread(target=self.update_timer_data, args=[round]).start()

    def update_timer_data(self, round):
        """countdown the timer for the game"""
        i = 60
        while i >= 0:
            time.sleep(1)
            self.send_time(str(i))
            i -= 1
        # reset timer back to null
        self.send_time(None)
        round.tabulate_round()

    def make_move(self, data):
        print('noooo')
        print('nevermind')
        print('received')
        print('cool')

    # ASYNC TO SYNC ACTIONS
    def send_update_game_players(self, game):
        """sends all game info as a json object when there's an update"""
        game = Game.objects.get(id=self.id)
        async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'update_game_players',
                        'game': game.as_json(),
                    }
                )

    def send_time(self, time):
        """sends the current time on the clock"""
        async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'update_timer',
                        'time': time,
                    }
                )

    # SEND DATA ACTIONS
    def update_game_players(self, username):
        self.send(text_data=json.dumps(username))

    def update_timer(self, timedata):
        """send timer data to the frontend"""
        self.send(text_data=json.dumps(timedata))

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    commands = {
        'update_game_players': update_game_players,
        'update_timer': update_timer,
        'LEAVE_GAME': leave_game,
        'NEW_MESSAGE': new_message,
        'START_ROUND': start_round,
        'MAKE_MOVE': make_move,
    }

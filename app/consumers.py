""" All of the websocket actions for the game and chat functionalities"""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Game, Message, GamePlayer


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

    def send_update_game_players(self, game):
        return async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'update_game_players',
                        'game': game.as_json(),
                    }
                )

    def join_game(self):
        user = self.scope['user']
        game = Game.objects.get(id=self.id)
        if not hasattr(user, 'gameplayer'):
            game_player = GamePlayer.objects.create(user=user, game=game)
            message = '{} joined'.format(user.username)
            Message.objects.create(
                message=message,
                game=game,
                game_player=game_player,
                message_type="action"
            )
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
            Message.objects.create(message=message, game=game, game_player=game_player, message_type="action")
            game_player.delete()
            self.send_update_game_players(game)

    def update_game_players(self, username):
        self.send(text_data=json.dumps(username))

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def new_message(self, data):
        user = self.scope['user']
        game_player = GamePlayer.objects.get(user=user)
        game = Game.objects.get(id=self.id)
        Message.objects.create(
            message=data['message'],
            message_type='user_message',
            game=game,
            game_player=game_player,
        )
        self.send_update_game_players(game)

    def start_round(self, data):
        user = self.scope['user']
        game_player = GamePlayer.objects.get(user=user)
        game_player.started = True
        game_player.save()
        messages = self.game.messages.all().order_by('created_at')
        self.send_update_game_players(self.game, messages)


    commands = {
        'update_game_players': update_game_players,
        'LEAVE_GAME': leave_game,
        'NEW_MESSAGE': new_message,
        'START_ROUND': start_round,
    }

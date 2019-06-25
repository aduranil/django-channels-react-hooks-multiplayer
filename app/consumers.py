""" All of the websocket actions for the game and chat functionalities"""
import json
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from .models import Game, Message, GamePlayer


class GameConsumer(WebsocketConsumer):
    """Websocket for inside of the game"""
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'game_%s' % self.id
        self.game = Game.objects.get(id=self.scope['url_route']['kwargs']['id'])
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

    def join_game(self):
        user = self.scope['user']
        game = Game.objects.get(id=self.id)
        user_in_game = bool([user == u for u in self.game.users.all()])
        messages = Message.objects.all().filter(game=self.id).order_by('created_at')
        if not user_in_game:
            self.game.users.add(user)
            game_player = GamePlayer.objects.create(user=user)
            self.game.game_players.add(game_player)
            self.game.save()
            message = '{} joined'.format(user.username)
            Message.objects.create(message=message, game=self.game, user=user, message_type="action")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_game_players',
                'players': [{'id': u.user.id, 'username': u.user.username, 'followers': u.followers, 'stories': u.stories, 'started': u.started} for u in self.game.game_players.all()],
                'messages': [m.as_json() for m in messages]
            }
        )

    def leave_game(self, data):
        user = self.scope['user']
        self.game.users.remove(user)
        for player in self.game.game_players.all():
            if player.id == user.id:
                self.game.game_players.remove(player)

        self.game.save()
        message = '{} left'.format(user.username)
        Message.objects.create(message=message, game=self.game, user=user, message_type="action")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_game_players',
                'players': [{'id': u.user.id, 'username': u.user.username, 'followers': u.followers, 'stories': u.stories, 'started': u.started} for u in self.game.game_players.all()],
            }
        )

    def update_game_players(self, username):
        self.send(text_data=json.dumps(username))
        print(username)

    def get_messages(self, messages):
        self.send(text_data=json.dumps(messages))

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.commands[data['command']](self, data)


    def new_message(self, data):
        user = self.scope['user']
        message = Message.objects.create(
            message=data['message'],
            message_type='user_message',
            game=self.game,
            user=user,
        )
        messages = Message.objects.all().filter(game=self.id).order_by('created_at')
        updated_messages = [m.as_json() for m in messages]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'get_messages',
                'messages': updated_messages,
            }
        )

    commands = {
        'update_game_players': update_game_players,
        'leave_game': leave_game,
        'NEW_MESSAGE': new_message,
        'get_messages': get_messages
    }

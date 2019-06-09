""" All of the websocket actions for the game and chat functionalities"""
import json
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from .models import Game, Message


class GameConsumer(WebsocketConsumer):
    """Websocket for inside of the game"""
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'game_%s' % self.id
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
        game.users.add(user)
        game.save()
        message = '{} joined'.format(user.username)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'join',
                'username': user.username,
            }
        )

    def leave_game(self, data):
        user = self.scope['user']
        game = Game.objects.get(id=self.id)
        game.users.remove(user)
        game.save()
        message = '{} left'.format(user.username)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'leave',
                'players': [{'id': u.id, 'username': u.username} for u in game.users.all()],
            }
        )

    def join(self, username):
        self.send(text_data=json.dumps(username))
        print(username)

    def leave(self, username):
        self.send(text_data=json.dumps(username))

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.commands[data['command']](self, data)

    # Receive message from room group
    # async def chat_message(self, event):
    #     message = event['message']
    #
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    commands = {
        'join': join,
        'leave_game': leave_game,
    }

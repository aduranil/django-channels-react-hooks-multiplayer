
import json

from app.models import Game
from app.serializers
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from django.http import HttpResponse

class GameCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        game = Game.objects.create(room_name=request.data['room_name'])
        game.users.add(user)
        return Response({
            'id': game.id,
            'room_name': game.room_name,
            'player': user.username,
        }, status=status.HTTP_201_CREATED)


class GameListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        game_objects = Game.objects.all().filter(game_status='active')
        games = [g.as_json() for g in game_objects]
        return HttpResponse(json.dumps(games), content_type="application/json")

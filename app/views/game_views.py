
import json

from app.models import Game
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
        return HttpResponse(json.dumps(game.as_json()), content_type="application/json")


class GameListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        game_objects = Game.objects.all().filter(game_status='active')
        games = [g.as_json() for g in game_objects]
        return HttpResponse(json.dumps(games), content_type="application/json")


class GameGetView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        game = Game.objects.get(id=id)
        return HttpResponse(json.dumps(game.as_json()), content_type="application/json")

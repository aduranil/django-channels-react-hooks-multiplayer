import json
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse

from app.models import Game, GamePlayer


class GameCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        game = Game.objects.create(room_name=request.data['room_name'])
        return HttpResponse(json.dumps(game.as_json()))


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
        return HttpResponse(json.dumps(game.as_json()))

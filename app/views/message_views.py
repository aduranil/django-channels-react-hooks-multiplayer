from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication

from django.http import HttpResponse

from app.models import Message

class MessageCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        message = Message.objects.create(room_name=request.data['room_name'])


class MessageGetView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        """get all the messages for a specific game"""
        messages = Message.objects.all().filter(game=1)
        return HttpResponse(json.dumps(messages.as_json()), content_type="application/json")

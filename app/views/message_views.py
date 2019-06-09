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


class MessageListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        message_objects = Message.objects.all()
        messages = [m.as_json() for m in message_objects]
        return HttpResponse(json.dumps(messages), content_type="application/json")

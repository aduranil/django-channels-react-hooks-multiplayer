from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from app.serializers import UserSerializer

from django.contrib.auth.models import User
from django.db import IntegrityError

class LoginUser(ObtainAuthToken):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=request.data['email'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': serializer.validated_data['username'],
                'email': serializer.validated_data['email'],
            }, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class GetUser(ObtainAuthToken):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
        })


class CreateUser(ObtainAuthToken):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    token = Token.objects.create(user=user)
                    response = serializer.data
                    response['token'] = token.key
                    return Response(response, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            import pdb; pdb.set_trace()
            return Response({'data': ''}, status=400)

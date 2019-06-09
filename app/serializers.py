from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User
from .models import Game

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=4)

    def create(self, validated_data):
        """Create and return a `User` with an email, username and password."""
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,)
    password = serializers.CharField(min_length=4)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

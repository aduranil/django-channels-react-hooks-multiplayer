from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,)
    username = serializers.CharField()
    password = serializers.CharField(min_length=4)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,)
    password = serializers.CharField(min_length=4)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

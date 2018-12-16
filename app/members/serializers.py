from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from members.backends import FacebookBackend

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
        )


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('아이디 또는 비밀번호가 올바르지 않습니다.')
        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data


class FacebookAuthTokenSerializer(serializers.Serializer):
    facebook_user_id = serializers.CharField()
    access_token = serializers.CharField()

    def validate(self, data):
        facebook_user_id = data['user_id']
        access_token = data['access_token']
        if User.objects.filter(username=facebook_user_id).exists():
            user = User.objects.get(username=facebook_user_id)
        else:
            user = get_user_by_access_token(access_token)

        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data
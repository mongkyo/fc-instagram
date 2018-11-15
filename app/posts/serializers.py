from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Post


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateField()


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer
    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'created_at',
            'modified_at',
            'like_users',
        )
        read_only_fields = (
            'author',
        )

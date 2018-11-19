from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Post, Comment, PostLike


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = (
            'author',
            'content',
        )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'created_at',
            'modified_at',
            'like_users',
            'comments',
        )
        read_only_fields = (
            'author',
        )


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = PostLike
        fields = (
            'post',
            'user',
        )
        read_only_fields = (
            'user',
        )
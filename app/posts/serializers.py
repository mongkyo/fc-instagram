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
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'created_at',
            'is_like',
        )
        read_only_fields = (
            'author',
        )
    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                postlike = obj.postlike_set.get(user=user)
                return PostLikeSerializer(postlike).data
            except PostLike.DoesNotExist:
                return



class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = PostLike
        fields = (
            'pk',
            'post',
            'user',
            'create_at',
        )
        read_only_fields = (
            'user',
        )


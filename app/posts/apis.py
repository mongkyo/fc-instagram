import json

from django.http import HttpResponse
from rest_framework import status, permissions, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.permissions import IsUser
from .serializers import PostSerializer, PostLikeSerializer
from .models import HashTag, Post, PostLike


class PostList(generics.ListCreateAPIView):
    permissions_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeCreateDestroy(APIView):
    permissions = (
        permissions.IsAuthenticated,
    )

    def post(self, request, post_pk):
        serializer = PostLikeSerializer(
            data={**request.data, 'post': post_pk},
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = get_object_or_404(PostLike, pk=post_pk)
        post_like = get_object_or_404(PostLike, post=post, user=request.user)
        post_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeCreateAPIView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class PostLikeDestroyAPIView(generics.DestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsUser,
    )





# class PostLikeCreate(generics.ListCreateAPIView):
#     permissions_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#     )
#     queryset = PostLike.objects.all()
#     serializer_class = PostLikeSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(auther=self.request.user)

class PostLikeDelete:
    pass


# class PostLikeDelete(generics.DestroyAPIView):
#     permissions_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#     )
#     queryset = PostLike.objects.all()
#     serializer_class = PostLikeSerializer


def tag_search(request):
    # URL: '/posts/api/tag-search/'
    # request.GET으로 전달된
    #  search_keyword값을 가지는(contains)
    #  HashTag목록을
    #  dict요소의 list로 만들어 HttpResponse에 리턴
    #  ex) [{}, {}, {}]
    keyword = request.GET.get('keyword', '')
    tags = []
    if keyword:
        tags = list(HashTag.objects.filter(name__istartswith=keyword).values())
    result = json.dumps(tags)
    return HttpResponse(result, content_type='application/json')

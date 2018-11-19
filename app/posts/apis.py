import json

from django.http import HttpResponse, Http404
from rest_framework import status, permissions, generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer
from .models import HashTag, Post, Comment, PostLike


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


class PostLikeCreate(APIView):
    permissions = (
        permissions.IsAuthenticated,
    )
    def post(self, request, post_pk):
        # URL1: /posts/like/
        # URL2: /posts/<post_pk>/like/
        # 특정 Post에 대해서
        # PostLike를 만든다
        #  조건 : request.user와 해당 Post에 연결된 PostLike가 없어야 함
        post = get_object_or_404(Post, pk=post_pk)
        # 위 user, post와 연결된 PostLike가 있는지
        if PostLike.objects.filter(user=request.user, post=post).exists():
            data = {
                'detail': '이미 좋아요를 누른 포스트입니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        post_like = PostLike.objects.create(user=request.user, post=post)
        return Response(status=status.HTTP_201_CREATED)

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

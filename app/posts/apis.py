import json

from django.http import HttpResponse, Http404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer
from .models import HashTag, Post


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


class PostLikeCreate:
    pass


class PostLikeDelete:
    pass


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

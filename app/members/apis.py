from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework.views import APIView

from members.backends import FacebookBackend
from .permissions import IsOwnerOrReadOnly
from .models import User
from .serializers import UserSerializer, AuthTokenSerializer


class AuthTokenView(APIView):
    """
    username, password를 받아서
    사용자 인증에 성공하면 해당 사용자와 연결된 토큰 정보와 사용자 정보를 동시에 리턴
    """
    def post(self, request):
        # request.data로 오는 데이터는 'username', 'password'
        # 그냥 Serializer (ModelSerializer아님)
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            # to_representation() 함수를 Serializer내에 정의
            # -> {'token': <Token key>, 'user': <해당 유저 정보 serializer>}
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacebookAuthTokenView(APIView):
    # URL: /members/api/facebook-auth-token/
    def post(self, request):

        # 전달받은 토큰(페이스북 access token)값과 유저ID(access_token, user_id)를 사용해서
        # 정상적인 token인지 검사 후 (access_token으로 받아온 정보의 id와 user_id가 같은지)
        # DB에 해당 유저가 존재하는지 검사(authenticate)
        # 있다면 -> 토큰 발급
        # 없다면 -> 유저 생성 후 토큰 발급
        #          -> 생성로직은 FacebookBackend참조

        # serializer = FacebookAuthTokenSerializer(data=request.data)
        # if serializer.is_valid():
        #     # to_representation() 함수를 Serializer내에 정의
        #     # -> {'token': <Token key>, 'user': <해당 유저 정보 serializer>}
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #
        facebook_user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')
        if User.objects.filter(username=facebook_user_id).exists():
            user = User.objects.get(username=facebook_user_id)
        else:
            user = FacebookBackend.get_user_by_access_token(access_token)
        token = Token.objects.get_or_create(user=user)[0]
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)


class UserDetailAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = request.user
            if not user.is_authenticated:
                raise NotAuthenticated()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_object(self):
        # 하나의 Object를 특정화 하기 위한 조건을 가진 필드명 또는 URL패턴명
        #  기본값: 'pk'
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        # 'pk'가 URL패턴명중에 없으면
        if lookup_url_kwarg not in self.kwargs:
            # 근데 인증된 상태도 아니라면
            if not self.request.user.is_authenticated:
                raise NotAuthenticated()
            return self.request.user

        # 'pk'가 URL패턴명에 있으면,
        # 기존 GenericAPIView에서의 동작을 그대로 실행
        return super().get_object()

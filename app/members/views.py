import imghdr
import io
import json
from pprint import pprint

import requests
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm, UserProfileForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages

User = get_user_model()


def login_view(request):
    # URL: /members/login/
    #   config.urls에서 '/members/'부분을 'members.urls'를 사용하도록 include
    #   members.urls에서 '/login/'부분을 이 view에 연결

    # Template: members/login.html
    #  템플릿의 GET요청시 아래의 LoginForm인스턴스를 사용
    #  POST요청시의 처리는 아직 하지 않음

    # Form: members/forms.py
    #   LoginForm
    #     Username, password를 받을 수 있도록 함
    #       password는 widget에 PasswordInput을 사용하기
    context={}
    if request.method == 'POST':
        # 1. reuqest.POST에 데이터가 옴
        # 2. 온 데이터 중에서 username에 해당하는 값과 password에 해당하는 값을 각각
        #    username,password변수에 할당
        # 3. 사용자 인증을 수행
        #    username/password에 해당하는 사용자가 있는지 확인
        # 4-1 인증에 성공한다면
        #    세션/쿠키 기반의 로그인 과정을 수행, 완료 후 posts:post-list 페이지로 redirect
        # 4-2 인증에 실패한다면
        #    이 페이지에서 인증에 실패했음을 사용자에게 알려줌
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post-list')
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'members/login.html', context)


def logout_view(request):
    # URL: /members/logout/
    # Template: 없음
    # !POST요청일 때만 처리
    # 처리 완료 후 'posts:post-list'로 이동
    # base.html에 있는 'Logout'버튼이 이 view로의 POST요청을 하도록 함
    #   -> form을 구현해야 함
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    # URL: /members/signup/
    # Template: members/singup.html
    # Form:
    #  SignupForm
    #    username, password1, password2를 받음
    # 나머지 요소들은 login.html의 요소를 최대한 재활용

    # GET요청시 해당 템플릿 보여주도록 처리
    # base.html에 있는 'Signup'버튼이 이 쪽으로 이동할 수 있도록 url 링크 걸기

        # 1. request.POST에 전달된 username, password1, password2를
        #    각각 해당 이름의 변수에 할당
        # 2-x 에서는 HttpResponse에 문자열로 에러를 리턴해주기
        #  2-1 username에 해당하는 User가 이미 있다면 사용자명 ({username})은 이미 사용중입니다.
        #  2-2 password1과 password2가 일치하지 않는다면,
        #      비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다.
        # 3. 위의 두 경우가 아니라면
        #    새 User를 생성, 해당 User로 로그인 시켜준 후 'posts:post-list'로 redirect처리


        # 짧게 만들기
        # render경우
        # 1. POST요청이며 사용자명이 이미 존재할 경우
        # 2. POST요청이며 비밀번호가 같지 않은 경우
        # 3. GET요청인 경우
        # redirect
        # 1. POST요청이며 사용자명이 존재하지 않고 비밀번호가 같은 경우


        # if request.method가 POST면:
        #     if 사용자명이 존재하면:
        #         render1
        #     if 비밀번호가 같지 않으면:
        #         render2
        #     (else, POST이면서 사용자명도 없고 비밀번호도 같으면):
        #         return redirect
        # (POST면서 사용자명이 존재하면)
        # (POST면서 비밀번호가 같지 않으면)
        # (POST면서 사용자명이 없고 비밀번호가 같은 경우가 "아니면" -> GET요청도 포함)
        # return render
    context = {}

    if request.method == 'POST':
        # POST로 전달된 데이터를 확인
        # 올바르다면 User를 생성하고 post-list화면으로 이동
        # (is_vaild()가 True면 올바르다고 가정)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post-list')
    # GET요청시 또는 POST로 전달된 데이터가 올바르지 않을 경우
    # signup.html에
    #   빈 Form또는 올바르지 않은 데이터에 대한 정보가 포함된 Form을 전달해서
    #   동적으로 Form을 랜더링
    else:
        form = SignupForm()

    context['form'] = form
    return render(request, 'members/signup.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # is_valid()를 통과하고 인스턴스 수정이 완료되면
            # messages모듈을 사용해서 템플릿에 수정완료 메시지를 표시
            # https://docs.djangoproject.com/en/2.1/ref/contrib/messages/
            messages.success(
                request,
                '프로필 수정이 완료되었습니다'
            )
    form = UserProfileForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'members/profile.html', context)


def facebook_login(request):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token?'
    api_me = f'{api_base}/me'
    code = request.GET.get('code')
    params = {
        'client_id': 185664342348143,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': 'ac46ae0b33da7268c5ab0c367ffa7961',
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    # # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
    # # json.loads는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 parsing해서 파이썬 Object를 리턴함
    #

    data = response.json()
    access_token = data['access_token']

    # # access_token을 사용해서 사용자 정보를 가져오기
    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'first_name',
            'last_name',
            'picture.type(large)',
        ])
    }
    response = requests.get(api_me, params)
    data = response.json()

    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_img_profile = data['picture']['data']['url']
    # HTTP GET요청의 응답을 받아옴
    img_response = requests.get(url_img_profile)
    img_data = img_response.content
    # 응답의 binary data를 사용해서 In-memory binary stream(file)객체를 생성
    # 이렇게 안하고 FileField가 지원하는 InMemoryUploadedFile객체를 사용하기!
    # f = io.BytesIO(img_response.content)

    # imghdr모듈을 사용해 Image binary data의 확장자를 알아냄
    ext = imghdr.what('', h=img_data)
    # Form에서 업로드한 것과 같은 형태의 file-like object생성
    #  첫 번째 인수로 반드시 파일명이 필요. <facebook_id>.<확장자>형태의 파일명을 지정
    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

    try:
        user = User.objects.get(username=facebook_id)
        # update_or_create
        user.last_name = last_name
        user.first_name = first_name
        # user.img_profile = f
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
            img_profile=f,
        )

    login(request, user)
    return redirect('posts:post-list')

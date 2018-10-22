from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # 인증 성공시
            login(request, user)
            return redirect('posts:post-list')
        else:
            # 인증 실패시
            pass
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
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
    if request.method == 'POST':
        pass
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, 'members/signup.html', context)

from django.shortcuts import render

from .models import Post


def post_list(request):
    # 1. Post모델에
    #   created_at (생성시간 저장)
    #   modified_at (수정시간 저장)
    #     두 필드를 추가

    # 2. Post모델이 기본적으로 pk 내림차순으로 정렬되도록 설정
    # 3. 모든 Post객체에 대한 QuerySet을
    #    render의 context인수로 전달 (키 : posts)

    # 4. posts/post_list.html을 Template으로 사용
    #       템플릿에서는 posts값을 순회하며
    #       각 Post의 photo정보를 출력

    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_create(request):
    # 1. posts/post_create.html 구현
    #   form구현
    #   input[type=file]
    #   button[type=submit]

    # 2. /posts/create/ URL에 이 view를 연결
    #    URL명은 'post-create'를 사용
    # 3. render를 적절히 사용해서 해당 템플릿을 return
    # 4. base.html의 nav부분에 '+ Add Post'텍스트를 갖는 a링크 하나 추가,
    #       {% url %} 테그를 사용해서 포스트 생성으로 링크 걸어주기
    return render(request, 'posts/post_create.html')

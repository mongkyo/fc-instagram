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

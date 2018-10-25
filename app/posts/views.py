from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Post
from .forms import PostCreateForm

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


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post-list')
    else:
        form = PostCreateForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    """
    post_pk에 해당하는 POST에 댓글을 생성하는 view
    'POST'메서드 요청만 처리

    'content'키로 돌아온 값을 사용해 댓글 생성. 작성자는 요청한 User
    URL: /posts/<post_pk>/comments/create/

    :param request:
    :param post_pk:
    :return:
    """
    context = {}
    if request.method == 'POST':
        pass
    return redirect('posts:post-list')

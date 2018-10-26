import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Post, Comment, HashTag
from .forms import PostCreateForm, CommentCreateForm, CommentForm, PostForm


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
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            if comment_content:
                post.comments.create(
                    author=request.user,
                    content=comment_content,
                )
            return redirect('posts:post-list')

    else:
        form = PostForm()

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

    # 1. post_pk에 해당하는 Post객체를 가져와 post변수에 할당
    # 2. request.POST에 전달된 'content'키의 값을 content변수에 할당
    # 3. Comment생성
    #     author: 현재 요청의 user
    #     post: post_pk에 해당하는 Post객체
    #     content: request.POST로 전달된 'content'키의 값
    # 4. posts:post-list로 redirect하기
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            # form.save(
            #     post=post,
            #     author=request.user,
            # )
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # comment가 가진 content속성에서
            # 해시태그에 해당하는 문자열들을 가져와서
            # HashTag객체를 가져오거나 생성(get_or_create)
            # 이후 comment.tags에 해당 객체들을 추가

            # 댓글 저장 후, content에 포함된 HashTag목록을 댓글의 tags속성에 set

            return redirect('posts:post-list')


def tag_post_list(request, tag_name):
    posts = Post.objects.filter(comments__tags__name=tag_name).distinct()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substituted_keyword)

from django.shortcuts import render, redirect

from members.models import User
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

    if request.method == 'POST':
        # request.FILES에 form에서 보낸 파일 객체가 들어있음
        # 새로운 post를 생성한다.
        # author는 User.objects.first()
        # photo는 request.FILES에 있는 내용을 적절히 꺼내서 쓴다
        # 완료된 후 posts:post-list로 redirect

        # 정답
        # post = Post(author=User.objects.first(), photo=request.FILES['photo'])
        # post.save()
        # return redirect('posts:post-list')

        Post.objects.create(author=User.objects.first(), photo=request.FILES['photo'])
        return redirect('posts:post-list')
    else:
        # GET요청의 경우, 빈 Form 인스턴스를 context에 담아서 전달
        # Template에서는 'form'키로 해당 form 인스턴스 속성을 사용가능
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)

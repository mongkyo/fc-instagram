import re

from django.db import models
from django.utils import timezone

# from members.models import User
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        # <AppName>.<ModelName>
        # 'members.User',
        # User,
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    photo = models.ImageField('사진', upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
        related_query_name='like_post',
    )
    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    def like_toggle(self, user):
        # 전달받은 user가 이 Post를 Like한다면 해제
        # 안되어있다면 Like처리
        pass


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comments',
    )
    author = models.ForeignKey(
        # 'members.User',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    content = models.TextField()
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해시태그 목록'
    )

    # Comment의 save()가 호출 될 때,
    # content의 값을 사용해서 이 필드를 자동으로 채운 후 저장하기
    _html = models.TextField('태그가 HTML화된 댓글 내용', blank=True)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        def save_html():
            self._html = re.sub(
                self.TAG_PATTERN,
                r'<a href="/explore/tags/\g<tag>/">#\g<tag></a>',
                self.content,
            )

        def save_tags():
            tags = [HashTag.objects.get_or_create(name=name)[0]
                    for name in re.findall(self.TAG_PATTERN, self.content)]
            self.tags.set(tags)

        save_html()
        super().save(*args, **kwargs)
        save_tags()
    @property
    def html(self):
        # 자신의 content속성값에서
        # "#태그명"에 해당하는 문자열을
        #  아래와 같이 변경
        #   <a href="/explore/tags/{태그명}>/">#{태그명}</a>
        # re.sub를 사용
        return self._html
        # 템플릿에서는 comment.content대신 comment.html을 출력

        # 숙제
        #  /explore/tags/{태그명}/ URL에서
        #  해당 태그를 가진 Posttag목록을 보여주는 view, url, template구현
        #  URL name: tag-post-list
        #  view:
        #       tag_post_list(request, tag_name)
        #  template:
        #       /posts/tag_post_list.html

        # base.html에 있는 검색창에 값을 입력하고 Enter시 (Submit)
        #  해당 값을 사용해 위에서 만든 view로 이동


class HashTag(models.Model):
    name = models.CharField('태그명', max_length=100, unique=True,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'


class PostLike(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{post_pk}] Like (User: {username})'.format(
            post_pk=self.post.pk,
            username=self.user.username,
        )

    class Meta:
        # 특정 User가 특정 Post를 좋아요 누른 정보는 unique해야함
        unique_together = (
            ('post', 'user'),
        )
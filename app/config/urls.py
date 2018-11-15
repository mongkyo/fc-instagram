"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from config import settings
from posts import apis
from posts.views import tag_post_list

urlpatterns_api = [
    path('posts/', apis.PostList.as_view()),
    path('posts/<int:pk>/', apis.PostDetail.as_view()),
]


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='posts:post-list'), name='index'),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('explore/tags/<str:tag_name>/', tag_post_list, name='tag-post-list'),
    path('members/', include('members.urls')),
    path('api/', include(urlpatterns_api)),
]
# MEDIA_URL로 시작하는 URL은 static()내의 serve() 함수를 통해 처리
# MEDIA_ROOT기준으로 파일을 검색함
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)


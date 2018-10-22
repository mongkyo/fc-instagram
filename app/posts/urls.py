from django.urls import path

from . import views

# 중복되는 것을 방지시켜줌
app_name = 'posts'


# config.urls에 연결되는 것이기 때문에 / 기호는 뒷쪽에 붙여주어야한다.
urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('create/', views.post_create, name='post-create')
]
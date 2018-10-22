from django.urls import path

from . import views

# 중복되는 것을 방지시켜줌
app_name = 'members'


# config.urls에 연결되는 것이기 때문에 / 기호는 뒷쪽에 붙여주어야한다.
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
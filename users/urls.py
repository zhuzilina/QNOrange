from django.urls import path
from . import views
"""users应用的urls配置 """

app_name = 'users'
urlpatterns = [
    path('', views.user_home_private, name='user_home_private'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('img/code/', views.auth_image_code, name='auth_image_code'),
    path('message/', views.show_messages, name='message'),
    path('info/', views.change_info, name='change_info'),
    path('sum_info/', views.sum_info, name='sum_info'),
]
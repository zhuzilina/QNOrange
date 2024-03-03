from django.urls import path
from . import views
"""weweb应用的urls配置 """

app_name = 'weweb'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('story/', views.story, name='story')
]
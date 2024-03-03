from django.urls import path

from . import views
"""topics应用的urls配置 """


app_name = 'topics'
urlpatterns = [
    path('', views.topic.topics_view, name='topics_view'),
    path('add/', views.topic.topic_add, name='topic_add'),
    path('<int:topic_id>/', views.topic.topic_view, name='topic_view'),
    path('delete/', views.topic.topic_delete, name='topic_delete'),
    path('like/', views.topic.topic_like, name='topic_like'),
    # talk的url
    # path('<int:topic_id>/talk_add/', views.talk_add, name='talk_add'),
    path('talk_add/', views.talk.talk_add, name='talk_add'),
    path('talks/<int:talk_id>/delete/', views.talk.talk_delete, name='talk_delete'),
    path('talks/like/', views.talk.talk_like, name='talk_like'),
    # response的url
    path('talks/response_add/', views.response.response_add, name='response_add'),
    path('responses/<int:response_id>/response_delete/', views.response.response_delete, name='response_delete'),
    path('responses/response_like/', views.response.response_like, name='response_like'),
]
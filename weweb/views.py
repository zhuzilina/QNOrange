from django.shortcuts import render
from topics.views.topic_utilitys import get_user_active


# Create your views here.
def index(request):
    return render(request, 'weweb/test.html')


def history(request):
    return render(request, 'weweb/histroy.html')


def about(request):
    user_active = get_user_active(request)
    return render(request, 'weweb/about.html', {'user_active': user_active})


def story(request):
    user_active = get_user_active(request)
    return render(request, 'weweb/story.html', {'user_active': user_active})

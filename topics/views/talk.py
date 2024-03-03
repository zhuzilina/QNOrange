from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from topics import models
from . import TopicsModalForm
from users.models import Message


@csrf_exempt
def talk_add(request):
    """添加评论"""
    # 处理post请求
    form = TopicsModalForm.TalkForm(request.POST)
    if form.is_valid():
        talk = form.save(commit=False)
        topic_id = form.cleaned_data['topic_id']
        talk.topic_id = topic_id
        talk.source = request.session['find_id']
        talk.save()
        # 推送消息
        if int(request.POST.get('author')) == int(request.session.get("find_id")):
            return JsonResponse({'status': True})
        data = request.POST.get('data')
        message = "评论了你的话题" + '"' + data + '..."'
        Message.objects.create(user_id=int(request.POST.get('author')),
                               message_type=0,
                               message_source=talk.id,
                               forward=topic_id,
                               message=message,
                               source=request.session.get("find_id"))
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def talk_delete(request, talk_id):
    """删除评论"""
    talk = models.Talk.objects.get(id=talk_id)
    topic_id = request.GET.get('topic_id')
    # 判断请求者身份
    if talk.source == request.session.get("find_id"):
        models.Talk.objects.get(id=talk_id).delete()
        return redirect(f'/topics/{topic_id}/')
    return redirect(f'/topics/{topic_id}/')

@csrf_exempt
def talk_like(request):
    """喜欢评论"""
    # 判断点赞否
    q1 = Message.objects.filter(source=request.session.get('find_id'))
    q2 = q1.filter(message_type=2)
    q3 = q2.filter(message_source=int(request.POST.get('talk_id')))
    if q3:
        return JsonResponse({'status': False})
    # 点赞
    topic_id = int(request.POST.get('topic_id'))
    talk_id = int(request.POST.get('talk_id'))
    data = request.POST.get('data')
    talk = models.Talk.objects.get(id=talk_id)
    talk.like += 1
    talk.save()
    # 推送消息
    if int(request.POST.get('author')) == int(request.session.get("find_id")):
        return JsonResponse({'status': True})
    message = "喜欢了你的评论" + '"' + data + '"'
    Message.objects.create(user_id=int(request.POST.get('author')),
                           message_type=2,
                           message_source=talk_id,
                           forward=topic_id,
                           message=message,
                           source=request.session.get("find_id"))
    return JsonResponse({'status': True})

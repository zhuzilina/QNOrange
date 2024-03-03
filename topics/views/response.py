from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from topics import models
from . import TopicsModalForm
from users.models import Message


@csrf_exempt
def response_add(request):
    form = TopicsModalForm.ResponseForm(request.POST)
    if form.is_valid():
        response = form.save(commit=False)
        response.talk_id = form.cleaned_data['talk_id']
        response.source = request.session['find_id']
        if int(form.cleaned_data['forward_id']) > 1:
            response.forward_id = form.cleaned_data['forward_id']
        response.save()
        # 推送消息
        if int(request.POST.get('author')) == int(request.session.get("find_id")):
            return JsonResponse({'status': True})
        data = request.POST.get('data')
        message = "回复了你的评论" + '"' + data + '..."'
        Message.objects.create(user_id=int(request.POST.get('author')),
                               message_type=0,
                               message_source=response.id,
                               forward=int(request.POST.get('topic_id')),
                               message=message,
                               source=request.session.get("find_id"))
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def response_delete(request, response_id):
    """删除回复"""
    response = models.Response.objects.get(id=response_id)
    topic_id = request.GET.get('topic_id')
    talk_id = request.GET.get('forward')
    # 验证请求者身份
    if response.source == request.session.get("find_id"):
        models.Response.objects.filter(id=response_id).delete()
        return redirect(f'/topics/{topic_id}/#talk_content_{talk_id}')
    return redirect(f'/topics/{topic_id}/#talk_content_{talk_id}')


@csrf_exempt
def response_like(request):
    """喜欢回复"""
    # 判断点赞否
    q1 = Message.objects.filter(source=request.session.get('find_id'))
    q2 = q1.filter(message_type=3)
    q3 = q2.filter(message_source=int(request.POST.get('response_id')))
    if q3:
        return JsonResponse({'status': False})
    # 点赞
    topic_id = int(request.POST.get('topic_id'))
    response_id = int(request.POST.get('response_id'))
    data = request.POST.get('data')
    response = models.Response.objects.get(id=response_id)
    response.like += 1
    response.save()
    # 推送消息
    if int(request.POST.get('author')) == int(request.session.get("find_id")):
        return JsonResponse({'status': True})
    message = "喜欢了你的回复" + '"' + data + '"'
    Message.objects.create(user_id=int(request.POST.get('author')),
                           message_type=3,
                           message_source=response_id,
                           forward=topic_id,
                           message=message,
                           source=request.session.get("find_id"))
    return JsonResponse({'status': True})
import time
import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from topics.models import Topic
from users.models import OurUser, Message
from .user_utilitys import replace_id

"""
负责用户主页响应的程序集
"""


def user_home_private(request):
    """处理用户个人页面响应"""
    if request.session.get('find_id'):
        # 获取用户信息
        user = OurUser.objects.get(id=request.session['find_id'])
        topics = Topic.objects.filter(owner_id=user.id)
        user.user_id = None
        user.password = None
        user_active = [user.id, user.user_name]
        # 随机选择一个头像
        user_photo = random.choice([
            '001.png',
            '002.png',
            '003.png',
            '004.webp',
            '005.png',
            '006.png',
            '007.png',
            '008.png',
            '009.png',
            '010.png',
            '011.png',
            '012.png',
            '013.png',
            '014.png',
            '015.png',
            '016.png',
            '017.png',
            '018.png',
            '019.png',
            '020.png',
            '021.webp',
        ])
        return render(request, 'users/user_home_private.html',
                      {'user': user, 'user_active': user_active, 'topics': topics, 'user_photo': user_photo})
    return redirect('/users/login/')


def change_name(request):
    """修改用户名"""
    # 判断用户名是存在
    if OurUser.objects.filter(user_name=request.POST.get('data')).exists():
        return False
    # 更新用户名
    user = OurUser.objects.get(id=request.session['find_id'])
    user.name = request.POST.get('data')
    user.save()
    return True


@csrf_exempt
def change_info(request):
    # 更改用户名
    print(request.POST.get('change_info'))
    if request.POST.get('change_info') == '1':
        if change_name(request):
            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'message': '用户名已存在！'})
    # 更改个性签名
    elif request.POST.get('change_info') == '2':
        user = OurUser.objects.get(id=request.session['find_id'])
        user.says = request.POST.get('data')
        user.save()
        return JsonResponse({'status': True})
    # 更改地址
    elif request.POST.get('change_info') == '5':
        user = OurUser.objects.get(id=request.session['find_id'])
        user.address = request.POST.get('data')
        user.save()
        return JsonResponse({'status': True})
    # 更改生日
    elif request.POST.get('change_info') == '4':
        user = OurUser.objects.get(id=request.session['find_id'])
        time_temp = request.POST.get('data')
        try:
            time_temp = time.strptime(time_temp, "%Y-%m-%d")
        except ValueError:
            return JsonResponse({'status': False, 'message': '请输入正确得时间！'})
        time_temp = int(time.mktime(time_temp))
        # 生日是否大于今天
        if time_temp < time.time():
            user.birthday = request.POST.get('data')
            user.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'message': '不能设置未来的时间'})
    # 更改性别
    elif request.POST.get('change_info') == '3':
        user = OurUser.objects.get(id=request.session['find_id'])
        print(request.POST.get('data'))
        try:
            gender = int(request.POST.get('data'))
        except ValueError:
            return JsonResponse({'status': False, 'message': '输入有误'})
        user.gender = gender
        user.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'message': '你的输入有误！'})


@csrf_exempt
def sum_info(request):
    """统计发帖数和点赞信息"""
    # 获取查询信息
    topics = Topic.objects.filter(owner_id=request.session['find_id'])
    messages = Message.objects.filter(user_id=request.session['find_id'])
    new_messages = messages.filter(visited=0)
    new_messages_account = len(new_messages)
    # 生成统计信息
    like_account, topic_account = 0, 0
    for topic in topics:
        like_account += topic.like
        topic_account += 1
    return JsonResponse({'status': True,
                         'like_account': like_account,
                         'topic_account': topic_account,
                         'message_account': new_messages_account})


@csrf_exempt
def show_messages(request):
    """显示用户消息"""
    # 获取查询信息
    messages = Message.objects.filter(user_id=request.session['find_id'])
    new_messages = messages.filter(visited=0)
    old_messages = messages.filter(visited=1)
    # 生成消息列表
    if messages:
        message_list = []
        if new_messages:
            for message in new_messages:
                message = replace_id(message)
                temp1 = f"<li class='list-group-item'><a href='../topics/{message.forward}"
                temp2 = f"/?new={message.id}'>{message.source}{message.message}</a></li>"
                temp3 = temp1 + temp2
                message_list.append(temp3)
        if old_messages:
            for message in old_messages:
                message = replace_id(message)
                temp1 = f"<li class='list-group-item'><a style='color:black;' href='../topics/{message.forward}"
                temp2 = f"/'>{message.source}{message.message}</a></li>"
                temp3 = temp1 + temp2
                message_list.append(temp3)
        strings = ''.join(message_list)
        strings = "<ul class='list-group list-group-flush'>" + strings + "</ul>"
        return JsonResponse({'status': True, 'messages': strings})
    return JsonResponse({'status': False})

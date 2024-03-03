from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from topics import models
from users.models import OurUser, Message
from . import topic_utilitys
from . import TopicsModalForm


def topics_view(request):
    """默认展示10个主题"""
    # 搜索主题
    search_data = request.GET.get('q', '')
    if search_data:
        # 返回搜索结果
        topics = models.Topic.objects.filter(title__contains=search_data)
        user_active = topic_utilitys.get_user_active(request)
        topics = topic_utilitys.abstract_content(topics)
        # 处理用户名
        topics = topic_utilitys.add_topic_name(topics)
        # 返回数据
        context = {'topics': topics, 'search_data': search_data, 'user_active': user_active}
        return render(request, 'topics/topics.html', context)
    # 正常情况访问页面数据
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    # 获取条目信息
    topics = models.Topic.objects.order_by('-date_added')[start:end]
    # 处理用户名
    topics = topic_utilitys.add_topic_name(topics)
    # 获取用户信息
    user_active = topic_utilitys.get_user_active(request)
    topics = topic_utilitys.abstract_content(topics)

    # 处理分页
    total_pages, div = divmod(models.Topic.objects.all().count(), 10)
    if div:
        total_pages += 1
    page_str_list = []
    plus = 5

    # 限制范围
    if total_pages <= 2 * plus:
        start_page = 1
        end_page = total_pages
    else:
        # 当前页小于plus时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus
        else:
            # 当前页大于plus时
            if page + plus > total_pages:
                start_page = total_pages - 2 * plus
                end_page = total_pages
            else:
                start_page = page - 5
                end_page = page + 5

    # 上一页
    if page - 1 > 0:
        ele = f"<li class='page-item'><a class='page-link' href=?page={page - 1}>上一页</a></li>"
        page_str_list.append(ele)
    # 中间页码
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = f"<li class='active page-item'><a class='page-link' href=?page={i}>{i}</a></li>"
        else:
            ele = f"<li class='page-item'><a class='page-link' href=?page={i}>{i}</a></li>"
        page_str_list.append(ele)
    # 下一页
    if page + 1 < total_pages:
        ele = f"<li class='page-item'><a class='page-link' href=?page={page + 1}>下一页</a></li>"
        page_str_list.append(ele)

    page_string = mark_safe(''.join(page_str_list))
    # 返回结果
    context = {'topics': topics,
               'user_active': user_active,
               'page_sting': page_string}
    return render(request, 'topics/topics.html', context)


def topic_view(request, topic_id):
    """展示一个主题的页面"""
    # 获取访问主题
    try:
        topic = models.Topic.objects.get(id=topic_id)
        # 处理用户名
        topic.temp_name = OurUser.objects.get(id=topic.owner_id).user_name
    except models.Topic.DoesNotExist:
        return HttpResponse('抱歉，您访问的页面不存在！', status=404)
    # 更新消息
    if request.GET.get('new'):
        message = Message.objects.get(id=int(request.GET.get('new')))
        message.visited = 1
        message.save()
    # 获取与主题相关联的话题
    talks = topic.talk_set.order_by('-date_added')
    talks = topic_utilitys.add_talk_name(talks)
    # 获取与话题有关的回复
    talk_list = []
    for talk in talks:
        talk_response = {}
        responses = talk.response_set.order_by('date_added')
        responses = topic_utilitys.add_response_name(responses)
        talk_response["talk"] = talk
        talk_response["responses"] = responses
        talk_list.append(talk_response)
    # 更新用户信息
    user_active = topic_utilitys.get_user_active(request)
    # 返回数据
    context = {'topic': topic, 'talk_list': talk_list, 'user_active': user_active}
    return render(request, 'topics/topic_new.html', context)


def topic_add(request):
    """添加主题"""
    # 没有数据，建立空表单
    user_active = topic_utilitys.get_user_active(request)
    if request.method == 'GET':
        form = TopicsModalForm.MyTopicForm
        return render(request, 'topics/topic_add.html', {'form': form, 'user_active': user_active})
    # POST提交数据，进行处理
    form = TopicsModalForm.MyTopicForm(request.POST)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.owner = OurUser.objects.get(id=request.session['find_id'])
        topic.save()
        return redirect('/topics/')
    return render(request, 'topics/topic_add.html', {'form': form, 'user_active': user_active})


def topic_delete(request):
    """删除主题"""
    topic_id = request.GET.get('id')
    topic = models.Topic.objects.get(id=topic_id)
    # 判断请求者身份
    if topic.owner_id == request.session['find_id']:
        models.Topic.objects.get(id=id).delete()
        return redirect('/topics/')
    return redirect('/topics/')


@csrf_exempt
def topic_like(request):
    """喜欢主题"""
    # 判断点赞否
    q1 = Message.objects.filter(source=request.session.get('find_id'))
    q2 = q1.filter(message_type=1)
    q3 = q2.filter(message_source=int(request.POST.get('topic_id')))
    if q3 or int(request.POST.get('author')) == int(request.session.get("find_id")):
        return JsonResponse({'status': False})
    # 点赞
    topic_id = int(request.POST.get('topic_id'))
    data = request.POST.get('data')
    topic = models.Topic.objects.get(id=topic_id)
    topic.like += 1
    topic.save()
    # 推送消息
    if int(request.POST.get('author')) == int(request.session.get("find_id")):
        return JsonResponse({'status': True})
    message = "喜欢了你的话题" + '"' + data + '"'
    Message.objects.create(user_id=int(request.POST.get('author')),
                           message_type=1,
                           message_source=topic_id,
                           forward=topic_id,
                           message=message,
                           source=request.session.get("find_id"))
    return JsonResponse({'status': True})

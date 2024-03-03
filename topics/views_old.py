# import re
#
# from django.http import Http404, HttpResponse, JsonResponse
# from django.shortcuts import render, redirect
# from django import forms
# from django.utils.safestring import mark_safe
# from django.views.decorators.csrf import csrf_exempt
#
# from topics import models
# from users.models import OurUser, Message
#
#
# # Create your views here.
# # 公共配置
# def _topic_page(obj):
#     """处理显示页数"""
#     page_list = []
#     data_size = obj.count()
#     for i in range(1, int(data_size / 10) + 2):
#         emt = f'<li class="page-item"><a class="page-link" href="?page={i}">{i}</a></li>'
#         page_list.append(emt)
#
#     if data_size / 10 > 10:
#         temp = page_list[:4] + ['...'] + page_list[-4:]
#         page_list = temp[:]
#     page_str = mark_safe(''.join(page_list))
#     return page_str
#
#
# def get_user_active(request):
#     """获取用户登录状态"""
#     return request.session.get('find_id'), request.session.get('user_name')
#
#
# def abstract_content(topics):
#     """压缩主题内容"""
#     temp = []
#     for topic in topics:
#         if len(topic.content) > 90:
#             topic.content = topic.content[:80] + "......"
#         temp.append(topic)
#     return temp
#
#
# class BootstrapModelForm(forms.ModelForm):
#     """定义使用bootstrap样式的ModelForm类"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             # field.widget.attrs ={'class':'form-control'}
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['style'] = 'margin-bottom: 1vh'
#             field.widget.attrs['placeholder'] = field.label
#
#
# # 表单功能支持
# class MyTopicForm(BootstrapModelForm):
#     """主题表单"""
#
#     class Meta:
#         model = models.Topic
#         fields = ['title', 'content']
#
#         widgets = {
#             'title': forms.Textarea(attrs={'rows': 2})
#         }
#
#
# class TalkForm(BootstrapModelForm):
#     """评论表单"""
#     topic_id = forms.CharField(widget=forms.HiddenInput())
#
#     class Meta:
#         model = models.Talk
#         fields = ['content']
#
#
# class ResponseForm(BootstrapModelForm):
#     """回复表单"""
#     talk_id = forms.CharField(widget=forms.HiddenInput())
#     forward_id = forms.CharField(widget=forms.HiddenInput(), required=False)
#
#     class Meta:
#         model = models.Response
#         fields = ['content']
#
#     def clean_forward_id(self):
#         if re.match(r'(^[-+]?([1-9][0-9]*|0)(\.[0-9]+)?$)', self.cleaned_data['forward_id']):
#             return self.cleaned_data['forward_id']
#         else:
#             return '1'
#
#
# # 主题功能
# def topics_view(request):
#     """默认展示10个主题"""
#     # 处理页面数据
#     page = int(request.GET.get('page', 1))
#     page_size = 10
#     start_index = (page - 1) * page_size
#     end_index = start_index + page_size
#     # 搜索主题
#     search_data = request.GET.get('q', '')
#     if search_data:
#         topics = models.Topic.objects.filter(title__contains=search_data)[start_index:end_index]
#         page_str = _topic_page(models.Topic.objects.filter(title__contains=search_data))
#         user_active = get_user_active(request)
#         topics = abstract_content(topics)
#         context = {'topics': topics, 'search_data': search_data, 'page_str': page_str, 'user_active': user_active}
#         return render(request, 'topics/topics.html', context)
#     # 正常情况访问页面数据
#     topics = models.Topic.objects.order_by('-date_added')[start_index:end_index]
#     page_str = _topic_page(models.Topic.objects.order_by('-date_added'))
#     user_active = get_user_active(request)
#     topics = abstract_content(topics)
#     context = {'topics': topics, 'page_str': page_str, 'user_active': user_active}
#     return render(request, 'topics/topics.html', context)
#
#
# def add_talk_name(talks):
#     _talks = []
#     for talk in talks:
#         s_id = talk.source
#         talk.source = OurUser.objects.get(id=s_id).user_name
#         _talks.append(talk)
#     return _talks
#
#
# def add_response_name(responses):
#     _responses = []
#     for response in responses:
#         s_id = response.source
#         f_id = response.forward
#         response.source = OurUser.objects.get(id=s_id).user_name
#         response.forward = [OurUser.objects.get(id=f_id).user_name, f_id]
#         _responses.append(response)
#     return _responses
#
#
# def topic_view(request, topic_id):
#     """展示一个主题的页面"""
#     try:
#         topic = models.Topic.objects.get(id=topic_id)
#     except models.Topic.DoesNotExist:
#         return HttpResponse('抱歉，您访问的页面不存在！', status=404)
#     # 获取与主题相关联的话题
#     talks = topic.talk_set.order_by('-date_added')
#     talks = add_talk_name(talks)
#     # 获取与话题有关的回复
#     talk_list = []
#     for talk in talks:
#         talk_response = {}
#         responses = talk.response_set.order_by('date_added')
#         responses = add_response_name(responses)
#         talk_response["talk"] = talk
#         talk_response["responses"] = responses
#         talk_list.append(talk_response)
#     user_active = get_user_active(request)
#     context = {'topic': topic, 'talk_list': talk_list, 'user_active': user_active}
#     return render(request, 'topics/topic_new.html', context)
#
#
# def topic_add(request):
#     """添加主题"""
#     # 没有数据，建立空表单
#     user_active = get_user_active(request)
#     if request.method == 'GET':
#         form = MyTopicForm
#         return render(request, 'topics/topic_add.html', {'form': form, 'user_active': user_active})
#     # POST提交数据，进行处理
#     form = MyTopicForm(request.POST)
#     if form.is_valid():
#         topic = form.save(commit=False)
#         topic.owner = OurUser.objects.get(id=request.session['find_id'])
#         topic.save()
#         return redirect('/topics/')
#     return render(request, 'topics/topic_add.html', {'form': form, 'user_active': user_active})
#
#
# def topic_delete(request):
#     """删除主题"""
#     id = request.GET.get('id')
#     topic = models.Topic.objects.get(id=id).delete()
#     return redirect('/topics/')
#
#
# @csrf_exempt
# def topic_like(request):
#     """喜欢主题"""
#     topic_id = int(request.POST.get('topic_id'))
#     content = request.POST.get('data')
#     topic = models.Topic.objects.get(id=topic_id)
#     topic.like += 1
#     topic.save()
#     message = "喜欢了你的话题" + '"' + content + '"'
#     Message.objects.create(user_id=int(request.POST.get('author')),
#                            message_type=1,
#                            forward=topic_id,
#                            message=message,
#                            source=request.session.get("find_id"))
#     return JsonResponse({'status': True})
#
#
# # 评论功能
# @csrf_exempt
# def talk_add(request):
#     """添加评论"""
#     # 处理post请求
#     form = TalkForm(request.POST)
#     if form.is_valid():
#         talk = form.save(commit=False)
#         topic_id = form.cleaned_data['topic_id']
#         talk.topic_id = topic_id
#         talk.source = request.session['find_id']
#         talk.save()
#         return JsonResponse({'status': True})
#     return JsonResponse({'status': False, 'error': form.errors})
#
#
# def talk_delete(request, talk_id):
#     """删除评论"""
#     models.Talk.objects.get(id=talk_id).delete()
#     topic_id = request.GET.get('topic_id')
#     return redirect(f'/topics/{topic_id}/')
#
#
# def talk_like(request, talk_id):
#     """喜欢评论"""
#     topic_id = request.GET.get('topic_id')
#     talk = models.Talk.objects.get(id=talk_id)
#     talk.like += 1
#     talk.save()
#     return redirect(f'/topics/{topic_id}/')
#
#
# # 回复功能
# @csrf_exempt
# def response_add(request):
#     form = ResponseForm(request.POST)
#     if form.is_valid():
#         response = form.save(commit=False)
#         response.talk_id = form.cleaned_data['talk_id']
#         response.source = request.session['find_id']
#         if int(form.cleaned_data['forward_id']) > 1:
#             response.forward_id = form.cleaned_data['forward_id']
#         response.save()
#         return JsonResponse({'status': True})
#     return JsonResponse({'status': False, 'error': form.errors})
#
#
# def response_delete(request, response_id):
#     """删除回复"""
#     topic_id = request.GET.get('topic_id')
#     models.Response.objects.filter(id=response_id).delete()
#     return redirect(f'/topics/{topic_id}')
#
#
# def response_like(request, response_id):
#     """喜欢回复"""
#     topic_id = request.GET.get('topic_id')
#     response = models.Response.objects.get(id=response_id)
#     response.like += 1
#     response.save()
#     return redirect(f'/topics/{topic_id}')

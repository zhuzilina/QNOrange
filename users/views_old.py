# import re
# import time
# from io import BytesIO
#
# from django import forms
# from django.core.exceptions import ValidationError
# from django.http import JsonResponse
# from django.shortcuts import render, HttpResponse, redirect
# from django.views.decorators.csrf import csrf_exempt
#
# from topics import models
# from utilitys.encripto import md5
# from utilitys.set_image import check_code
# from .models import OurUser, Message
#
#
# # Create your views here.
# # 公共配置
# class BootstrapModelForm(forms.ModelForm):
#     """定义使用bootstrap样式的ModelForm类"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#             field.widget.attrs = {'class': 'form-control', 'placeholder': f'请输入{field.label}'}
#
#
# # 用户功能
# def user_home_private(request):
#     """处理用户个人页面响应"""
#     if request.session.get('find_id'):
#         user = OurUser.objects.get(id=request.session['find_id'])
#         topics = models.Topic.objects.filter(owner_id=user.id)
#         user.user_id = None
#         user.password = None
#         user_active = [user.id, user.user_name]
#         return render(request, 'users/user_home_private.html',
#                       {'user': user, 'user_active': user_active, 'topics': topics})
#     return redirect('/users/login/')
#
#
# def user_home_public(request):
#     """处理用户公共动态页面响应"""
#     return render(request, 'users/user_home_public.html')
#
#
# class LoginForm(forms.Form):
#     """为用户登录提供表单"""
#     user_id = forms.CharField(label="账号",
#                               widget=forms.TextInput(attrs={
#                                   'class': 'form-control',
#                                   'placeholder': '输入手机号',
#                                   'id': 'Input1',
#                               }),
#                               )
#     password = forms.CharField(label="密码",
#                                widget=forms.PasswordInput(attrs={
#                                    'class': 'form-control',
#                                    'placeholder': '输入密码',
#                                    'id': 'Input2',
#                                }),
#                                )
#     code = forms.CharField(label="验证码",
#                            widget=forms.TextInput(attrs={
#                                'class': 'form-control',
#                                'placeholder': '输入验证码',
#                                'id': 'Input3',
#                            }),
#                            )
#
#
# def user_login(request):
#     """处理用户登录响应"""
#     if request.method == 'GET':
#         form = LoginForm()
#         return render(request, 'users/user_login.html', {'form': form})
#     # 处理post请求
#     form = LoginForm(request.POST)
#     if form.is_valid():
#         user_id = form.cleaned_data['user_id']
#         password = md5(form.cleaned_data['password'])
#         code = form.cleaned_data['code']
#         image_code = request.session.get('code')
#         print(image_code)
#
#         if image_code:
#             if code.upper() != image_code.upper():
#                 form.add_error('code', '验证码错误')
#                 return render(request, 'users/user_login.html', {'form': form})
#             if OurUser.objects.filter(user_id=user_id, password=password).exists():
#                 find_id = OurUser.objects.get(user_id=user_id).id
#                 user_name = OurUser.objects.get(user_id=user_id).user_name
#                 request.session['find_id'] = find_id
#                 request.session['user_id'] = user_id
#                 request.session['user_name'] = user_name
#                 request.session.set_expiry(60 * 60 * 24 * 7)
#                 return redirect('/topics/')
#             form.add_error('password', '密码或账号错误！')
#         form.add_error('code', '验证码失效，请重新输入！')
#     return render(request, 'users/user_login.html', {'form': form})
#
#
# def user_logout(request):
#     request.session.clear()
#     return redirect("/users/login")
#
#
# # 用户注册
# class OurUserForm(BootstrapModelForm):
#     """提供用户注册的表单"""
#     confirm = forms.CharField(widget=forms.PasswordInput, label="确认密码")
#     check_code = forms.CharField(label="验证码", required=True)
#
#     class Meta:
#         model = OurUser
#         fields = ('user_id', 'user_name', 'password', 'confirm', 'gender', 'birthday', 'address', 'check_code')
#         widgets = {
#             'password': forms.PasswordInput(
#             ),
#             'gender': forms.Select()
#         }
#
#     # 验证数据
#     def clean_user_id(self):
#         data = self.cleaned_data['user_id']
#         print(data)
#         ret = re.match(r"^1[3-9]\d{9}$", data)
#         print(ret)
#         if not ret:
#             raise ValidationError("手机号格式有误！")
#         if OurUser.objects.filter(user_id=data).exists():
#             raise ValidationError("手机号已存在！")
#         return data
#
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         return md5(password)
#
#     def clean_confirm(self):
#         password = self.cleaned_data['password']
#         if password != md5(self.cleaned_data['confirm']):
#             raise ValidationError('输入密码不一致！')
#         return md5(self.cleaned_data['confirm'])
#
#
# def user_register(request):
#     """处理注册响应"""
#     if request.method == 'GET':
#         form = OurUserForm()
#         return render(request, 'users/user_register.html', {'form': form})
#
#     # 处理post请求
#     form = OurUserForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['check_code']
#         img_code = request.session['code']
#         if code.upper() == img_code.upper():
#             request.session.clear()
#             form.save()
#             return redirect('/users/login/')
#     return render(request, 'users/user_register.html', {'form': form})
#
#
# def auth_image_code(request):
#     """处理图形验证码响应"""
#     stream = BytesIO()
#     img, strs = check_code()
#     img.save(stream, 'png')
#
#     # 将验证码写入cookie
#     request.session['code'] = strs
#     # 给session设置60s超时
#     request.session.set_expiry(60)
#
#     return HttpResponse(stream.getvalue(), content_type='image')
#
#
# @csrf_exempt
# def message_box(request):
#     content = []
#     for i in range(100):
#         tag1 = f"<a href='#'>第{i}条消息</a>"
#         tag2 = f"<div class='bg-transparent shadow jumbotron' style='margin-top: 1vh;height:3vh'>"
#         tag3 = f"</div>"
#         content.append(tag2 + tag1 + tag3)
#     content = ''.join(content)
#     return JsonResponse({'status': True, 'content': content})
#
#
# def change_name(request):
#     """修改用户名"""
#     print(OurUser.objects.filter(user_name=request.POST.get('data')).exists())
#     if OurUser.objects.filter(user_name=request.POST.get('data')).exists():
#         return False
#     user = OurUser.objects.get(id=request.session['find_id'])
#     user.name = request.POST.get('data')
#     user.save()
#     return True
#
#
# @csrf_exempt
# def change_info(request):
#     # 更改用户名
#     print(request.POST.get('change_info'))
#     if request.POST.get('change_info') == '1':
#         if change_name(request):
#             return JsonResponse({'status': True})
#         return JsonResponse({'status': False, 'message': '用户名已存在！'})
#     # 更改个性签名
#     elif request.POST.get('change_info') == '2':
#         user = OurUser.objects.get(id=request.session['find_id'])
#         user.says = request.POST.get('data')
#         user.save()
#         return JsonResponse({'status': True})
#     # 更改地址
#     elif request.POST.get('change_info') == '5':
#         user = OurUser.objects.get(id=request.session['find_id'])
#         user.address = request.POST.get('data')
#         user.save()
#         return JsonResponse({'status': True})
#     # 更改生日
#     elif request.POST.get('change_info') == '4':
#         user = OurUser.objects.get(id=request.session['find_id'])
#         time_temp = request.POST.get('data')
#         try:
#             time_temp = time.strptime(time_temp, "%Y-%m-%d")
#         except ValueError:
#             return JsonResponse({'status': False, 'message': '请输入正确得时间！'})
#         time_temp = int(time.mktime(time_temp))
#         if time_temp < time.time():
#             user.birthday = request.POST.get('data')
#             user.save()
#             return JsonResponse({'status': True})
#         return JsonResponse({'status': False, 'message': '不能设置未来的时间'})
#     elif request.POST.get('change_info') == '3':
#         user = OurUser.objects.get(id=request.session['find_id'])
#         print(request.POST.get('data'))
#         try:
#             gender = int(request.POST.get('data'))
#         except ValueError:
#             return JsonResponse({'status': False, 'message': '输入有误'})
#         user.gender = gender
#         user.save()
#         return JsonResponse({'status': True})
#     else:
#         return JsonResponse({'status': False, 'message': '你的输入有误！'})
#
#
# @csrf_exempt
# def sum_info(request):
#     """统计发帖数和点赞信息"""
#     topics = models.Topic.objects.filter(owner_id=request.session['find_id'])
#     like_account, topic_account = 0, 0
#     for topic in topics:
#         like_account += topic.like
#         topic_account += 1
#     return JsonResponse({'status': True, 'like_account': like_account, 'topic_account': topic_account})
#
#
# def replace_id(obj):
#     """替换用户名"""
#     obj.source = OurUser.objects.get(id=obj.source).user_name
#     return obj
# @csrf_exempt
# def show_messages(request):
#     """显示用户消息"""
#     messages = Message.objects.filter(user_id=request.session['find_id'])
#     print(messages)
#     if messages:
#         message_list = []
#         for message in messages:
#             message = replace_id(message)
#             temp = f"<li class='list-group-item'><a href='../topics/{message.forward}/'>{message.source}{message.message}</a></li>"
#             message_list.append(temp)
#         strings = ''.join(message_list)
#         strings = "<ul class='list-group list-group-flush'>" + strings + "</ul>"
#         return JsonResponse({'status': True, 'messages': strings})
#     return JsonResponse({'status': False})
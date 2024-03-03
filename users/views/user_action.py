from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse

from .user_utilitys import md5, check_code
from users.models import OurUser
from .UserModalForm import LoginForm, RegisterForm

"""
负责用户登录和注册的程序集
"""


def auth_image_code(request):
    """处理图形验证码响应"""
    stream = BytesIO()
    img, strs = check_code()
    img.save(stream, 'png')

    # 将验证码写入cookie
    request.session['code'] = strs
    # 给session设置60s超时
    request.session.set_expiry(60)

    return HttpResponse(stream.getvalue(), content_type='image')


def user_login(request):
    """处理用户登录响应"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/user_login.html', {'form': form})
    # 处理post请求
    form = LoginForm(request.POST)
    if form.is_valid():
        user_id = form.cleaned_data['user_id']
        password = md5(form.cleaned_data['password'])
        code = form.cleaned_data['code']
        image_code = request.session.get('code')
        # 匹配验证码
        if image_code:
            if code.upper() != image_code.upper():
                form.add_error('code', '验证码错误')
                return render(request, 'users/user_login.html', {'form': form})
            # 用户是否存在
            if OurUser.objects.filter(user_id=user_id, password=password).exists():
                find_id = OurUser.objects.get(user_id=user_id).id
                user_name = OurUser.objects.get(user_id=user_id).user_name
                request.session['find_id'] = find_id
                request.session['user_name'] = user_name
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('/topics/')
            form.add_error('password', '密码或账号错误！')
        form.add_error('code', '验证码失效，请重新输入！')
    return render(request, 'users/user_login.html', {'form': form})


def user_logout(request):
    """处理注销响应"""
    request.session.clear()
    return redirect("/users/login")


def user_register(request):
    """处理注册响应"""
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/user_register.html', {'form': form})

    # 处理post请求
    form = RegisterForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['check_code']
        img_code = request.session['code']
        # 匹配验证码
        if code.upper() == img_code.upper():
            request.session.clear()
            form.save()
            return redirect('/users/login/')
    return render(request, 'users/user_register.html', {'form': form})

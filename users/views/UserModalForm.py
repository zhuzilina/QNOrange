import re

from django import forms
from django.core.exceptions import ValidationError

from .user_utilitys import md5
from users.models import OurUser


class BootstrapModelForm(forms.ModelForm):
    """定义使用bootstrap样式的ModelForm类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': f'请输入{field.label}'}


class LoginForm(forms.Form):
    """为用户登录提供表单"""
    # 登录的输入组
    user_id = forms.CharField(label="账号",
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': '输入手机号',
                                  'id': 'Input1',
                              }),
                              )
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '输入密码',
                                   'id': 'Input2',
                               }),
                               )
    code = forms.CharField(label="验证码",
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': '输入验证码',
                               'id': 'Input3',
                           }),
                           )


class RegisterForm(BootstrapModelForm):
    """提供用户注册的表单"""
    # 注册表单的额外输入组
    confirm = forms.CharField(widget=forms.PasswordInput, label="确认密码")
    check_code = forms.CharField(label="验证码", required=True)

    class Meta:
        model = OurUser
        fields = ('user_id', 'user_name', 'password', 'confirm', 'gender', 'birthday', 'address', 'check_code')
        widgets = {
            'password': forms.PasswordInput(
            ),
            'gender': forms.Select()
        }

    # 验证用户手机号
    def clean_user_id(self):
        data = self.cleaned_data['user_id']
        print(data)
        ret = re.match(r"^1[3-9]\d{9}$", data)
        print(ret)
        if not ret:
            raise ValidationError("手机号格式有误！")
        if OurUser.objects.filter(user_id=data).exists():
            raise ValidationError("手机号已存在！")
        return data

    # 验证用户登录密码
    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

    # 验证用户登录密码确认
    def clean_confirm(self):
        password = self.cleaned_data['password']
        if password != md5(self.cleaned_data['confirm']):
            raise ValidationError('输入密码不一致！')
        return md5(self.cleaned_data['confirm'])

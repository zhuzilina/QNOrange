from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class OurUser(models.Model):
    """定义用户数据表"""
    user_id = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    password = models.CharField(max_length=100, verbose_name='密码')
    user_name = models.CharField(max_length=20, verbose_name='昵称')
    choices_gender = [
        (1, '男'),
        (2, '女')
    ]
    gender = models.SmallIntegerField(choices=choices_gender, verbose_name='性别', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='地区')
    says = models.CharField(max_length=100, null=True, blank=True, verbose_name='个性签名')

    def __str__(self):
        return self.user_name


class Message(models.Model):
    """定义消息数据表"""
    user = models.ForeignKey(OurUser, on_delete=models.CASCADE)
    message_type = models.SmallIntegerField()
    message_source = models.SmallIntegerField(default=0)
    message = models.CharField(max_length=200)
    source = models.SmallIntegerField()
    forward = models.SmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    visited = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'messages'

    def __str__(self):
        return self.message

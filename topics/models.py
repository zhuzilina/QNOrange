from django.db import models
from users.models import OurUser


# Create your models here.
class Topic(models.Model):
    """主题的数据表"""
    title = models.CharField(max_length=20, verbose_name="主题")
    content = models.TextField(max_length=2000, verbose_name="内容")
    date_added = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    owner = models.ForeignKey(OurUser, on_delete=models.CASCADE)

    temp_name = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        """return the string of model"""
        return self.title


class Talk(models.Model):
    """主题的评论的数据表"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, verbose_name="内容")
    date_added = models.DateTimeField(auto_now_add=True)
    source = models.IntegerField(default=1)
    like = models.IntegerField(default=0)
    temp_name = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'talks'

    def __str__(self):
        """return the string of model"""
        return self.content[:20] + "..."


class Response(models.Model):
    """回复评论的数据表"""
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE)
    forward = models.IntegerField(default=1)
    source = models.IntegerField(default=1)
    content = models.CharField(max_length=200, verbose_name="你的评论")
    date_added = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    temp_name = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'responses'

    def __str__(self):
        """return the string of model"""
        return self.content[:20] + "..."

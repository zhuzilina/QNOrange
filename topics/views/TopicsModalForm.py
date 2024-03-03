import re

from django import forms

from topics import models


class BootstrapModelForm(forms.ModelForm):
    """定义使用bootstrap样式的ModelForm类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.widget.attrs ={'class':'form-control'}
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'margin-bottom: 1vh'
            field.widget.attrs['placeholder'] = field.label


# 表单功能支持
class MyTopicForm(BootstrapModelForm):
    """主题表单"""

    class Meta:
        model = models.Topic
        fields = ['title', 'content']

        widgets = {
            'title': forms.Textarea(attrs={'rows': 2})
        }


class TalkForm(BootstrapModelForm):
    """评论表单"""
    topic_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = models.Talk
        fields = ['content']


class ResponseForm(BootstrapModelForm):
    """回复表单"""
    talk_id = forms.CharField(widget=forms.HiddenInput())
    forward_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.Response
        fields = ['content']

    def clean_forward_id(self):
        if re.match(r'(^[-+]?([1-9][0-9]*|0)(\.[0-9]+)?$)', self.cleaned_data['forward_id']):
            return self.cleaned_data['forward_id']
        else:
            return '1'

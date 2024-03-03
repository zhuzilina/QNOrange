from users.models import OurUser


def get_user_active(request):
    """获取用户登录状态"""
    return request.session.get('find_id'), request.session.get('user_name')


def abstract_content(topics):
    """压缩主题内容"""
    temp = []
    for topic in topics:
        if len(topic.content) > 90:
            topic.content = topic.content[:80] + "......"
        temp.append(topic)
    return temp


def add_topic_name(topics):
    """替换主题的用户id"""
    _topic = []
    for topic in topics:
        s_id = topic.owner_id
        topic.temp_name = OurUser.objects.get(id=s_id).user_name
        _topic.append(topic)
    return _topic

def add_talk_name(talks):
    """替换评论的用户id"""
    _talks = []
    for talk in talks:
        s_id = talk.source
        talk.temp_name = OurUser.objects.get(id=s_id).user_name
        _talks.append(talk)
    return _talks


def add_response_name(responses):
    """替换回复的用户id"""
    _responses = []
    for response in responses:
        s_id = response.source
        f_id = response.forward
        response.temp_name = (OurUser.objects.get(id=s_id).user_name, OurUser.objects.get(id=f_id).user_name)
        _responses.append(response)
    return _responses

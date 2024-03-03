from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

none_login_url = [
    '/users/login/',
    '/users/login',
    '/users/register',
    '/users/register/',
    '',
    '/',
    '/topics/',
    '/topics',
    '/users/img/code/',
    '/history/',
    '/history',
]


class Auth(MiddlewareMixin):
    """验证登录"""

    def process_request(self, request):
        if request.path_info in none_login_url:
            return
        user_id = request.session.get('find_id')
        if user_id:
            return
        return redirect('/users/login')
    # def process_response(self, request, response):

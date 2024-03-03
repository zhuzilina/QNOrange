# from django.conf import settings
# import hashlib
#
#
# # 加密密码
# def md5(data_string):
#     obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
#     obj.update(data_string.encode('utf-8'))
#     return obj.hexdigest()
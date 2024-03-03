import hashlib
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from django.conf import settings

from users.models import OurUser

"""
为users应用提供支持的程序集
"""


def check_code(width=120, height=30, char_length=5, font_file='/web/QNOrange/static/arial.ttf', font_size=28):
    """生成随机数和随机图片"""
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """生成随机字母"""
        return chr(random.randint(65, 90))

    def rndColor():
        """生成随机颜色"""
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


def replace_id(obj):
    """替换用户名"""
    obj.source = OurUser.objects.get(id=obj.source).user_name
    return obj


def md5(data_string):
    """加密密码"""
    # 加盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # 加密文明文
    obj.update(data_string.encode('utf-8'))
    # 生成md5
    return obj.hexdigest()

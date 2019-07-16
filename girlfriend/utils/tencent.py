# -*- coding: utf-8 -*-
"""腾讯AI平台请求通用函数"""

import time
import random
import string
import base64
import hashlib
from urllib import parse

import requests


USERAGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}


def get_time_stamp():
    """生成请求时间戳"""
    return int(time.time())

def get_nonce_str():
    """生成随机字符串"""
    return ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 16)))

def md5_encode(app_id):
    """生成会话标识
    :param app_id => 应用标识
    """
    if not isinstance(app_id, str):
        app_id = str(app_id)
    md5 = hashlib.md5()
    md5.update(app_id.encode('utf-8'))
    encoded_str = md5.hexdigest().upper()
    return encoded_str

def get_request_sign(parser, app_key):
    """获取请求签名
    :param app_key => 应用标识
    """
    params = sorted(parser.items())
    uri_str = parse.urlencode(params, encoding="UTF-8")
    sign_str = '{}&app_key={}'.format(uri_str, app_key)
    hash_md5 = hashlib.md5(sign_str.encode("UTF-8"))
    return hash_md5.hexdigest().upper()

def get_base64(pic_param):
    """获取媒体的Base64字符串
    :param media_param => 媒体URL或者图片文件的BufferedReader对象
    """
    if isinstance(pic_param, str):
        pic_data = requests.get(pic_param, headers=USERAGENT).content
    elif hasattr(pic_param, 'read'):
        pic_data = pic_param.read()
    else:
        raise TypeError('The picture media must be URL or BufferedReader.')
    # 将图片内容进行转码存储
    image = base64.b64encode(pic_data).decode("utf-8")
    return image

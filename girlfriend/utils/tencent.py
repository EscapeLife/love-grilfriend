# -*- coding: utf-8 -*-
"""腾讯AI平台请求通用函数"""

import time
import random
import string
import hashlib
from urllib import parse


def get_time_stamp():
    """生成请求时间戳"""
    return int(time.time())

def get_nonce_str():
    """生成随机字符串"""
    return ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 16)))

def md5_encode(text):
    """生成会话标识"""
    if not isinstance(text, str):
        text = str(text)
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    encoded_str = md5.hexdigest().upper()
    return encoded_str

def get_request_sign(parser, app_key):
    """获取请求签名"""
    params = sorted(parser.items())
    uri_str = parse.urlencode(params, encoding="UTF-8")
    sign_str = '{}&app_key={}'.format(uri_str, app_key)
    hash_md5 = hashlib.md5(sign_str.encode("UTF-8"))
    return hash_md5.hexdigest().upper()

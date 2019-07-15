# -*- coding: utf-8 -*-
"""
利用腾讯AI平台实现一个自动回复的聊天机器人

Usage:
    CHATBOT = Chatbot(app_id='123456', app_key='123456')
    print(CHATBOT.get_chat_text('爱自己女朋友就是爱自己'))
"""

import time
import random
import string

import requests

from girlfriend.utils.tencent import md5_encode, get_request_sign


class Chatbot:
    """腾讯聊天机器人"""
    def __init__(self, app_id=None, app_key=None):
        self.app_id = app_id
        self.app_key = app_key
        self.nonce_str = self.get_nonce_str()
        self.time_stamp = self.get_time_stamp()
        self.tencent_ai_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

    @classmethod
    def get_nonce_str(cls):
        """生成随机字符串"""
        return ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 16)))

    @classmethod
    def get_time_stamp(cls):
        """生成请求时间戳"""
        return int(time.time())

    def get_chat_text(self, text):
        """获取返回的聊天信息"""
        if self.app_id is None or self.app_key is None:
            print('The app_id or app_key is none, please check.')
        params = {
            'app_id': self.app_id,               # 应用标识
            'time_stamp': self.time_stamp,       # 请求时间戳(秒级)
            'nonce_str': self.nonce_str,         # 随机字符串
            'session': md5_encode(self.app_id),  # 会话标识
            'question': text                     # 用户输入的聊天内容
        }
        params['sign'] = get_request_sign(params, self.app_key) # 签名信息

        response = requests.get(self.tencent_ai_url, params=params)
        if response.status_code == 200:
            data_dict = response.json()
            if data_dict['ret'] == 0:
                return data_dict['data']['answer']
            print('The tencent smart chat failed to get data:{}'.format(data_dict['msg']))
        return 'The tencent ai platform interface call failed.'

# -*- coding: utf-8 -*-
"""
利用腾讯AI平台实现一个自动回复的聊天机器人

Usage:
    from girlfriend.components.ai_robot import Chatbot
    it = Chatbot('your_app_id', 'your_app_key')
    it.run('text')
"""

from urllib import parse
import requests

from girlfriend.utils.tencent import get_time_stamp, get_nonce_str
from girlfriend.utils.tencent import md5_encode, get_request_sign

CONTENTTYPE = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

class Chatbot:
    """腾讯聊天机器人"""
    def __init__(self, app_id=None, app_key=None):
        self.app_id = app_id
        self.app_key = app_key
        self.tencent_chat_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

    def make_params(self, text):
        """获取调用接口的参数"""
        if self.app_id is None or self.app_key is None:
            print('The app_id or app_key is none, please check.')
        params = {
            'app_id': self.app_id,               # 应用标识
            'time_stamp': get_time_stamp(),      # 请求时间戳(秒级)
            'nonce_str': get_nonce_str(),        # 随机字符串
            'session': md5_encode(self.app_id),  # 会话标识
            'question': text                     # 用户输入的聊天内容
        }
        params['sign'] = get_request_sign(params, self.app_key)  # 签名信息
        return params

    def run(self, text):
        """执行方法(可多次执行)"""
        params = self.make_params(text)
        response = requests.post(self.tencent_chat_url,
                                 data=parse.urlencode(params).encode("utf-8"),
                                 headers=CONTENTTYPE)
        if response.status_code == 200:
            data_dict = response.json()
            if data_dict['ret'] == 0:
                print(data_dict['data']['answer'])

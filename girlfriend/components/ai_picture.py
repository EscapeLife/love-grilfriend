# -*- coding: utf-8 -*-
"""
利用腾讯AI平台识别图片内容信息并自动生成文字描述

Usage:
    from girlfriend.components.ai_picture import PicToText
    it = PicToText('your_app_id', 'your_app_key')
    it.run('URL' or 'FileObj')
"""

from urllib import parse
import requests

from girlfriend.utils.tencent import get_time_stamp, get_nonce_str
from girlfriend.utils.tencent import get_request_sign, get_base64

CONTENTTYPE = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


class PicToText:
    """看图说话"""
    def __init__(self, app_id=None, app_key=None):
        self.app_id = app_id
        self.app_key = app_key
        self.tencent_pic_url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_imgtotext'

    def make_params(self, pic_param):
        """获取调用接口的参数"""
        if self.app_id is None or self.app_key is None:
            print('The app_id or app_key is none, please check.')
        params = {
            'app_id': self.app_id,           # 应用标识
            'time_stamp': get_time_stamp(),  # 请求时间戳(秒级)
            'nonce_str': get_nonce_str(),    # 随机字符串
            'image': get_base64(pic_param),  # 用户输入的聊天内容
            'session_id': get_time_stamp()   # 会话标识
        }
        params['sign'] = get_request_sign(params, self.app_key)  # 签名信息
        return params

    def run(self, pic_param):
        """执行方法(可多次执行)"""
        params = self.make_params(pic_param)
        response = requests.post(self.tencent_pic_url,
                                 data=parse.urlencode(params).encode("utf-8"),
                                 headers=CONTENTTYPE)
        if response.status_code == 200:
            data_dict = response.json()
            if data_dict['ret'] == 0:
                print(data_dict['data']['text'])

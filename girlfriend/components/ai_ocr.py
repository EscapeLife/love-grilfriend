# -*- coding: utf-8 -*-
"""
利用腾讯AI平台实现实现图片的识别和提取
Usage:
    from girlfriend.components.ai_ocr import PictureOCR
    it = PictureOCR('your_app_id', 'your_app_key')
    it.run('URL' or 'FileObj')
"""

from urllib import parse
import requests

from girlfriend.utils.tencent import get_time_stamp, get_nonce_str
from girlfriend.utils.tencent import get_request_sign, get_base64

CONTENTTYPE = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


class PictureOCR:
    """识别图片转文字"""
    def __init__(self, app_id=None, app_key=None, image_path=None, image_name=None):
        self.app_id = app_id
        self.app_key = app_key
        self.image_path = image_path
        self.image_name = image_name

    def make_params(self, pic_param):
        """获取调用接口的参数"""
        if self.app_id is None or self.app_key is None:
            print('The app_id or app_key is none, please check.')
        params = {
            'app_id': self.app_id,           # 应用标识
            'image': get_base64(pic_param),  # 图片内容
            'card_type': 0,                  # 仅识别正面照片
            'time_stamp': get_time_stamp(),  # 请求时间戳(秒级)
            'nonce_str': get_nonce_str()     # 随机字符串
        }
        params['sign'] = get_request_sign(params, self.app_key)  # 签名信息
        return params

    def id_card_run(self, pic_param):
        """识别身份证图片(正面照片)(可多次执行)"""
        id_card_url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_idcardocr'
        params = self.make_params(pic_param)
        response = requests.post(id_card_url,
                                 data=parse.urlencode(params).encode("utf-8"),
                                 headers=CONTENTTYPE)
        if response.status_code == 200:
            data_dict = response.json()
            if data_dict['ret'] == 0:
                id_card_data = data_dict['data']
                print(', '.join([id_card_data['name'], id_card_data['sex'],
                                 id_card_data['nation'], id_card_data['birth'],
                                 id_card_data['address'], id_card_data['id']]))

# -*- coding: utf-8 -*-
"""
利用腾讯万象优图平台实现图片的识别和提取

项目地址
https://github.com/tencentyun/image-python-sdk-v2.0
"""

from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers


class CloudImage:
    """万象优图(付费服务)"""
    def __init__(self, app_id, secret_id, secret_key, bucket,
                 image_surface=None, image_url=None, image_file=None):
        self.app_id = app_id
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket = bucket
        self.image_surface = image_surface
        self.image_url = image_url
        self.image_file = image_file

    def get_client(self):
        """获取连接对象"""
        client = Client(self.app_id, self.secret_id, self.secret_key, self.bucket)
        client.use_http()
        client.set_timeout(30)
        return client

    def id_card_url_ocr(self):
        """OCR-URL-身份证识别"""
        client = self.get_client()
        if len(self.image_url) >= 0 and self.image_surface == 'front':
            # 返回正面URL图片信息
            print(client.idcard_detect(CIUrls(self.image_url), 0))
        elif len(self.image_url) >= 0 and self.image_surface == 'backend':
            # 返回反面URL图片信息
            print(client.idcard_detect(CIUrls(self.image_url), 1))

    def id_card_file_ocr(self):
        """OCR-File-身份证识别"""
        client = self.get_client()
        if len(self.image_file) >= 0 and self.image_surface == 'front':
            # 返回正面文件图片信息
            print(client.idcard_detect(CIUrls(self.image_file), 0))
        elif len(self.image_file) >= 0 and self.image_surface == 'backend':
            # 返回反面文件图片信息
            print(client.idcard_detect(CIUrls(self.image_file), 1))

    def id_card_diff_ocr(self):
        """OCR-身份证识别对比"""
        client = self.get_client()
        if len(self.image_url) >= 0:
            # 身份证URL图片信息
            print(client.face_idcardcompare('ID CARD NUM', 'NAME', CIUrl(self.image_url[0])))
        if len(self.image_file) >= 0:
            # 身份证文件图片信息
            print(client.face_idcardcompare('ID CARD NUM', 'NAME', CIFile(self.image_file[0])))

    def image_as_yellow_ocr(self):
        """OCR-图片鉴黄"""
        client = self.get_client()
        if len(self.image_url) >= 0:
            # URL图片信息
            print(client.porn_detect(CIUrls(self.image_url)))
        if len(self.image_file) >= 0:
            # 文件图片信息
            print(client.porn_detect(CIFiles(self.image_file)))

    def business_card_ocr(self):
        """OCR-名片识别"""
        client = self.get_client()
        if len(self.image_url) >= 0:
            # URL图片信息
            print(client.namecard_detect(CIUrls(self.image_url)))
        if len(self.image_file) >= 0:
            # 文件图片信息
            print(client.namecard_detect(CIFiles(self.image_file)))

    def face_detection(self):
        """Face-人脸检测"""
        client = self.get_client()
        if len(self.image_url) >= 0:
            # URL图片信息
            print(client.face_detect(CIUrls(self.image_url)))
        if len(self.image_file) >= 0:
            # 文件图片信息
            print(client.face_detect(CIFiles(self.image_file)))

    def facial_detection(self):
        """Face-五官定位"""
        client = self.get_client()
        if len(self.image_url) >= 0:
            # URL图片信息
            print(client.face_shape(CIUrls(self.image_url), 1))
        if len(self.image_file) >= 0:
            # 文件图片信息
            print(client.face_shape(CIFiles(self.image_file), 1))

    def face_diff(self):
        """Face-人脸对比"""
        client = self.get_client()
        if len(self.image_url) >= 0:
            # URL图片信息
            print(client.face_compare(CIFile(self.image_url[0]), CIFile(self.image_url[1])))
        if len(self.image_file) >= 0:
            # 文件图片信息
            print(client.face_compare(CIUrl(self.image_url[0]), CIUrl(self.image_url[1])))
        if len(self.image_url) >= 0 and len(self.image_file) >= 0:
            # URL图片信息和文件图片信息
            print(client.face_compare(CIUrl(self.image_url[0]), CIFile(self.image_file[0])))

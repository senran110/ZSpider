"""
@file:login.py
@time:2020/2/10-13:23
"""
import base64
import hashlib
import hmac
import json
import re
import time
from copy import deepcopy
from urllib.parse import urlencode

import requests
from http import cookiejar  # 用于保存登陆的cookie

# from PIL import Image

from const import *


class ZhihuLogin:
    def __init__(self):
        self.LOGIN_URL = 'https://www.zhihu.com/signin'
        self.LOGIN_API = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.verify_code_api = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"

        self.username = username  # 账号
        self.password = password  # 密码
        self.checkname = checkname  # 用户名，用于验证登陆

        self.login_data = FORM_DATA

        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar('../../cookie.txt')  # 保存的cookie文件

    def _check_user_pass(self):
        """
        检查用户名和密码是否已输入，若无则手动输入
        """
        if self.username.isdigit() and '+86' not in self.username:
            self.username = '+86' + self.username

    def _get_captcha(self, lang: str):
        """
        请求验证码
        :param lang:
        :return:
        """
        resp = self.session.get(self.verify_code_api, headers=headers)
        show_captcha = re.search(r'true', resp.text)
        if show_captcha:
            put_resp = self.session.put(self.verify_code_api, headers=headers)
            img_base64 = re.findall(
                r'"img_base64":"(.+)"', put_resp.text, re.S)[0].replace(r'\n', '')
            with open('./captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img_base64))

            # img = Image.open('./captcha.jpg')
            capt = input('请输入图片里的验证码：')
            # 这里必须先把参数 POST 验证码接口
            self.session.post(self.verify_code_api, data={'input_text': capt}, headers=headers)
            return capt
        else:
            return ''

    def _get_signature(self, timestamp):
        """
        通过 Hmac计算返回签名,参数是几个固定字符串加时间戳
        :param timestamp
        :return: signature
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()

    def get_encrypt_dict(self):
        """
        获取加密用的键值对
        :return:
        """
        timestamp = str(int(time.time() * 1000))
        signature = self._get_signature(timestamp)

        self.login_data.update({
            'captcha': self._get_captcha(self.login_data['lang']),
            'timestamp': timestamp,
            'signature': signature,
            'username': self.username,
            'password': self.password,
        })

        print(self.login_data)

    @staticmethod
    def get_encrypt_data(form_data: dict):
        """
        生成POST需要的加密数据
        :param form_data:
        :return:
        """
        data = {
            'param': urlencode(form_data)
        }
        resp = requests.post(encrypt_data_api, data=data)
        return resp.text

    def check_login(self):
        """
        实现一个检查登录状态的方法，如果访问登录页面出现跳转，说明已经登录成功
        :return:
        """
        resp = self.session.get(self.LOGIN_URL, allow_redirects=False, headers=headers)
        # Redirecting to <a href="https://www.zhihu.com">https://www.zhihu.com</a>.
        if resp.status_code == 302:
            print(requests.utils.dict_from_cookiejar(self.session.cookies))
            self.session.cookies.save()
            return True

        return False

    def _get_xsrf(self):
        """
        从登录页面获取 xsrf
        :return: str
        """
        self.session.get('https://www.zhihu.com/', allow_redirects=False)

        for c in self.session.cookies:
            if c.name == '_xsrf':
                return c.value

        raise AssertionError('获取 xsrf 失败')

    def load_cookies(self):
        """
        读取 Cookies 文件加载到 Session
        :return: bool
        """
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except FileNotFoundError:
            return False

    def run(self, load_cookies: bool = True):
        if load_cookies and self.load_cookies():
            print('读取 Cookies 文件')
            if self.check_login():
                print('登录成功')
                return True

            print('Cookies 已过期')

        self._check_user_pass()
        self.get_encrypt_dict()
        data = self.get_encrypt_data(self.login_data)
        headers_ = deepcopy(headers)

        headers_.update({
            'content-type': 'application/x-www-form-urlencoded',
            'x-zse-83': '3_2.0',
            'x-xsrftoken': self._get_xsrf()
        })

        resp = self.session.post(self.LOGIN_API, data=data, headers=headers_)
        print(resp.json())

        if 'error' in resp.text:
            print(json.loads(resp.text)['error'])
        if self.check_login():
            print('登录成功')
            return True

        print('登录失败')
        return False


if __name__ == '__main__':
    zh = ZhihuLogin()
    zh.run()

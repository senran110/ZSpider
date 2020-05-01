"""
@file:Qmingpian.py
@time:2019/7/28-13:18
"""
import os
import pickle
import execjs
import base64
import json
import requests

from Qlogin import login_selenium, check_login
from util import telephone, headers


class QMP:
    def __init__(self):
        self.product_api = "https://vipapi.qimingpian.com/DataList/productListVip"
        self.index_url = "https://www.qimingpian.com/finosda/project/pinvestment"

        self.data = {
            "time_interval": "",
            "tag": "",
            "tag_type": "and",
            "province": "",
            "lunci": "",
            "page": 1,
            "num": 20,
            "unionid": ""
        }
        self.headers = headers
        self.session = requests.session()
        self.telephone = telephone

    def q_login(self):
        """
        模拟登录企名片, 存在cookie文件则读取，否则再次模拟登录
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        :return:
        """
        if os.path.exists("cookies.pkl"):
            file_cookies = pickle.load(open("cookies.pkl", "rb"))
            # 测试cookies是否失效
            text = check_login(file_cookies)
            if "充值" not in text:
                login_selenium(self.index_url, self.telephone)
        else:
            login_selenium(self.index_url, self.telephone)

        file_cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in file_cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

            if cookie['name'] == 'gw_unionid':
                print(f"unionid:{cookie['value']}")
                self.data['unionid'] = cookie['value']

    def get_product_data(self):
        """
        请求接口获取加密数据
        :return:
        """
        page = 1
        while True:
            resp = self.session.post(self.product_api, headers=self.headers, data=self.data)
            product_dict = resp.json()
            if product_dict['status'] == 0:
                page = page + 1
                encrypt_data = product_dict.get("encrypt_data")
                self.decrypt_data(encrypt_data)
                self.data['page'] = page
            else:
                print(resp.text)
                print("查看更多数据需要认证...")
                break

    @staticmethod
    def decrypt_data(encrypt_data):
        """
        对加密数据进行解密
        :param encrypt_data:
        :return:
        """
        # with open('server/Qmingpian.js') as f:
        #     js_encrypt = f.read()
        # ctx_encrypt = execjs.compile(js_encrypt)

        local_api = "http://localhost:8000/data"
        data = {
            "encrypt": encrypt_data
        }

        decrypt_data = requests.post(local_api, data=data)
        # 防止JS返回字符串内有特殊编码的字符将它转成base64再return返回，Python再进行解码获取数据
        decrypt_data = base64.b64decode(decrypt_data.text)
        json_data = json.loads(decrypt_data)
        for i, value in enumerate(json_data['list']):
            print(i, value['product'], value['hangye1'], value['yewu'], value['money'])

    def __call__(self, *args, **kwargs):
        self.q_login()
        self.get_product_data()


if __name__ == '__main__':
    qmp = QMP()
    qmp()


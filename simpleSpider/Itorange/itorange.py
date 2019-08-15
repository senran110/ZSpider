"""
@file:itorange.py
@time:2019/8/7-14:45
"""

# 登录链接:https://www.itjuzi.com/api/authorizations
# account: "xxxx"
# password: "11111111111111"
# type: "pswd"
# ------------
# city: []
# com_fund_needs: ""
# hot_city: ""
# keyword: ""
# location: ""
# page: 1
# pagetotal: 0
# per_page: 20
# prov: ""
# round: []
# scope: ""
# selected: ""
# sort: ""
# status: ""
# sub_scope: ""
# total: 0
# year: []
import json
import copy
import pymongo
from configparser import ConfigParser
from pprint import pprint
from fake_useragent import UserAgent

import requests

ua = UserAgent()


class ItOrange:
    def __init__(self):
        self.login_api = "https://www.itjuzi.com/api/authorizations"
        self.user_api = "https://www.itjuzi.com/api/users/user_header_info"
        self.spider_url = "https://www.itjuzi.com/company/"
        self.spider_api = "https://www.itjuzi.com/api/companys"
        # 股东信息等同理构造api请求
        self.detail_api = "https://www.itjuzi.com/api/companies/{0}?type=basic"  # 用于获取较为详细公司信息

        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "Referer": "https://www.itjuzi.com/company",
            "Host": "www.itjuzi.com"
        }
        self.company_params = {
            "city": [],
            "com_fund_needs": "",
            "hot_city": "",
            "keyword": "",
            "location": "",
            "page": 1,
            "pagetotal": 0,
            "per_page": 30,
            "prov": "",
            "round": [],
            "scope": "",
            "selected": "",
            "sort": "",
            "status": "",
            "sub_scope": "",
            "total": 0,
            "year": []
        }
        # self.company_params = {
        #     "page": 4,
        #     "pagetotal": 0,
        #     "per_page": 30,
        # }
        self.session = requests.session()
        self.userName, self.passWord = ItOrange.read_config()
        self.client = pymongo.MongoClient('localhost', 27017)
        self.collection = self.client.SPIDER.Orange

    def login_get_token(self):
        data = {
            "account": self.userName,
            "password": self.passWord,
            "type": "pswd"
        }
        # Request payload
        # resp = self.session.post(self.login_api, data=json.dumps(data), headers=self.headers)
        resp = self.session.post(self.login_api, json=data, headers=self.headers)
        # resp.headers.get('Set-Cookie')
        Json_token = resp.json()
        Token = Json_token['data']['token']

        return Token

    def set_cookie_user(self, token):
        headers = copy.deepcopy(self.headers)
        headers['Authorization'] = token

        resp = self.session.get(self.user_api, headers=headers)
        user_info_json = resp.json()
        user_id = user_info_json.get('data').get('user_id')
        # 保持手动构建的cookies,用update方法更新cookie就行了Cookie: juzi_user=; juzi_token=bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3Lml0anV6aS5jb21cL2FwaVwvYXV0aG9yaXphdGlvbnMiLCJpYXQiOjE1NjUyMjg3NzMsImV4cCI6MTU2NTIzMjM3MywibmJmIjoxNTY1MjI4NzczLCJqdGkiOiI5N0RabXFzdWJobGxwQ3dLIiwic3ViIjo3NDQ5NzksInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.4COkFICHZZcFP8efVvpR7NKzBkcBaMfht_GAVDycX1g
        cookie_dict = {
            "juzi_user": str(user_id),
            "juzi_token": token
        }
        self.session.cookies.update(cookie_dict)

    def get_company_data(self, token):
        headers = copy.deepcopy(self.headers)
        page = 0
        headers['Authorization'] = token
        while True:
            headers['User-Agent'] = ua.random
            company_info_list = self.session.post(self.spider_api, json=self.company_params, headers=headers).json()
            # 若请求成功
            if company_info_list.get('code') == 200:
                company_data = company_info_list.get('data').get('data')
                total_page = company_info_list.get('data').get("page").get("total")
                # 根据条数求页数就是要请求的api链接数
                max_page = (total_page // len(company_data)) + 1 if total_page % len(company_data) else total_page // 30
                # 根据总条数获取请求次数
                for company in company_data:
                    item = dict()
                    item['id'] = company.get('id')
                    item['name'] = company.get('name')
                    item['city'] = company.get('city')
                    item['register_name'] = company.get('register_name')
                    item['scope'] = company.get('scope')
                    item['slogan'] = company.get('slogan')
                    item['round'] = company.get('round')
                    item['detail_url'] = self.spider_url + str(item['id'])
                    detail_company_api = self.detail_api.format(item['id'])
                    results = self.get_company_detail_info(detail_company_api, headers, item)
                    # 不存在则插入，存在则不操作
                    self.collection.update({"id": results['id']}, {'$setOnInsert': results}, upsert=True)

                page = page + 1
                if page <= max_page:
                    print("next:", page)
                    self.company_params['page'] = page
                else:
                    break
            else:
                # 非VIP只能采集前三页
                print("request error")
                break

    def get_company_detail_info(self, detail_company_api, headers, item):
        detail_info = self.session.get(detail_company_api, headers=headers).json()
        if detail_info['code'] == 200:
            basic_data = detail_info.get('data').get('basic')
            item['com_born_date'] = basic_data.get('com_born_date')
            item['com_fund_needs_name'] = basic_data.get('com_fund_needs_name')
            item['com_round_name'] = basic_data.get('com_round_name')
            item['com_des'] = basic_data.get('com_des')
        return item

    @staticmethod
    def read_config():
        # 读取配置文件信息
        cfg = ConfigParser()
        cfg.read('orange_config.ini')
        userName = cfg.get('userInfo', 'userName')
        passWord = cfg.get('userInfo', 'passWord')

        return userName, passWord

    def run(self):
        token = self.login_get_token()
        self.set_cookie_user(token)
        self.get_company_data(token)


if __name__ == '__main__':
    orange = ItOrange()
    orange.run()

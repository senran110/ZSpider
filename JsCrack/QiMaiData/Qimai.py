"""
@file:Qimai.py
@time:2019/8/1-9:21
"""
# r=f[Ja](f[Me](m, b))
# b  "00000008d78d46a"
# e -a[Gt](f[Rl])(T)
# m 的生成函数---三参+URL 后缀+e 生成 m

# 1、获取选择项列表 https://api.qimai.cn/rank/marketList?
# 2、根据主分类和子分类选择 https://api.qimai.cn/rank/marketRank?
# 3、构造参数请求列表 以及 翻页接口
import copy
import datetime
import os
import pickle
from pprint import pprint

import pymongo
import requests
from requests.utils import dict_from_cookiejar

from Qlogin import QiMainLogin, headers, COOKIEFILE


class DataList:
    def __init__(self):
        cookies_in_file = self.read_cookies()
        client = pymongo.MongoClient(host='localhost', port=27017)

        self.lxb = QiMainLogin()
        self.collection = client.SPIDER.QIMAI
        # 先从文件读取cookie判断是否有效,若无效则登录
        self.session = requests.session()

        self.loginError = 0
        if cookies_in_file and self.lxb.check_login(cookies_in_file):
            self.session.cookies = cookies_in_file
        else:
            print("Now ReLogin")
            cookiesjar = self.lxb.login_qimai()
            if cookiesjar is None:
                print("登录失败,请检查用户名密码")
                self.loginError = 1
            else:
                self.session.cookies = cookiesjar
        # GET
        self.market_url = "https://www.qimai.cn/rank/marketRank"
        self.marketList_api = "https://api.qimai.cn/rank/marketList"
        self.marketRank_api = "https://api.qimai.cn/rank/marketRank"
        self.headers = copy.deepcopy(headers)

    def read_cookies(self):
        if os.path.exists(COOKIEFILE):
            with open(COOKIEFILE, "rb") as f:
                # 将字典转换成RequestsCookieJar，赋值给session的cookies.
                cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            return cookies
        else:
            return None

    def request_marketList(self):
        # 首先获取analysis的值
        analysis = self.lxb.get_my_analysis(self.market_url, self.marketList_api)
        params = {
            "analysis": analysis
        }
        # print("3:", dict_from_cookiejar(self.session.cookies))
        resp = self.session.get(self.marketList_api, params=params, headers=self.headers)
        # pprint(resp.json()) # 看数字的意义 取消注释

    # https://api.qimai.cn/rank/marketRank?analysis=dTBlTyx0dQV8ZHEEdDB2CCpZeBRUdwlHUwJmSwZwVBFuB1hdU11mXHATFxZWVg8bWwBCW1VEYlFeUyQUDF0MD1MDAwkABgNwG1U%3D&market=6&category=14&country=cn&collection=topselling_free&date=2019-08-04
    def request_marketRank(self):
        # 若登录失败则退出
        if self.loginError:
            return
        # 6代表华为 14代表商务 看全部见request_marketList
        market_id = input("输入大分类数字如6>>") 
        category_id = input("输入子分类数字如14>>")
        # date = input("输入日期>>")
        #             "analysis": analysis,
        #             # "collection": "topselling_free",
        #             # "country": "cn",
        params = {
            "market": market_id,
            "category": category_id,
            "date": datetime.date.today().strftime('%Y-%m-%d')
        }

        page = 1
        maxPage = 0

        while True:
            if page != 1:
                params['country'] = 'cn'
                params['collection'] = 'topselling_free'
                params.pop('analysis')
            params_list = list(params.values())

            analysis = self.lxb.get_my_analysis(self.market_url, self.marketRank_api, params=params_list)
            params['analysis'] = analysis
            resp = self.session.get(self.marketRank_api, params=params, headers=self.headers)
            results = resp.json()
            if maxPage == 0:
                maxPage = int(results.get("maxPage"))
                print("maxPage:", maxPage)

            if results.get("code") == 10000:
                rankInfos = results.get("rankInfo")
                for rankInfo in rankInfos:
                    item = dict()
                    item['appName'] = rankInfo.get('appInfo').get('appName')
                    item['publisher'] = rankInfo.get('appInfo').get('publisher')
                    item['app_comment_score'] = rankInfo.get('appInfo').get('app_comment_score')
                    item['app_comment_count'] = rankInfo.get('appInfo').get('app_comment_count')
                    self.save_to_mongo(item)
            else:
                print("error in rank:", results)

            page = page + 1
            if page > maxPage:
                print("exit")
                break
            else:
                print("continue")
                params['page'] = str(page)

    def save_to_mongo(self, item):
        self.collection.insert_one(item)


if __name__ == '__main__':
    market = DataList()
    market.request_marketList()
    market.request_marketRank()

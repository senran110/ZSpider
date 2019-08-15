"""
@file:douban.py
@time:2019/8/15-10:36
"""
from pprint import pprint

import requests
import execjs
import re

if __name__ == '__main__':
    url = "https://book.douban.com/subject_search?search_text=%E5%95%86%E4%B8%9A&cat=1001&start=15"
    response = requests.get(url=url)

    r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)

    # 导入js
    with open('doubanSearch.js', 'r', encoding="utf8") as f:
        decrypt_js = f.read()

    ctx = execjs.compile(decrypt_js)

    data = ctx.call('decrypt', r)
    # pprint(data)
    print(data['payload']['text'], data['payload']['total'])
    print("-----"*10)
    for item in data['payload']['items']:
        print(item['title'], "--", item['abstract'])

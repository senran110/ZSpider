import re

import requests
from requests.exceptions import ConnectionError


class FastIpSpider:
    def __init__(self):
        self.url = 'http://www.kuaidaili.com/free/inha/{}/'
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }

    def get_page(self, url, options={}):
        """
        访问指定页面，并返回response
        :param url:
        :param options:
        :return:
        """
        headers = dict(self.base_headers, **options)

        print(f'正在抓取:{url}')
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f'抓取成功:{url}')
                return response.text
            else:
                print(f"{url},状态码不合法 {response.status_code}")
                return None
        except ConnectionError:
            print(f'抓取失败:{url}')
            return None

    def parse_ip(self, page):
        url = self.url.format(page)
        html = self.get_page(url)
        if html:
            ip_address = re.compile('<td data-title="IP">(.*?)</td>')

            re_ip_address = ip_address.findall(html)

            port = re.compile('<td data-title="PORT">(.*?)</td>')

            re_port = port.findall(html)

            for address, port in zip(re_ip_address, re_port):
                address_port = address + ':' + port
                yield address_port.replace(' ', '')


def middleware(ip):
    yield from ip.parse_ip(1)


if __name__ == '__main__':
    ip = FastIpSpider()
    for i in middleware(ip):
        print(i)

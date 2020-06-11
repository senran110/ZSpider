"""
@file:myadsl.py
@time:2019/9/17-10:33
"""
import re
import requests
import time

import platform

from redisDB import RedisClient
from .config import *

if platform.python_version().startswith('2.'):
    import commands as subprocess
elif platform.python_version().startswith('3.'):
    import subprocess
else:
    raise ValueError('python version must be 2 or 3')


class Sender:
    def __init__(self):
        self.timer = time.time()

    def get_ip(self, ifname=ADSL_IFNAME):
        """
        获取本机ip
        :param ifname:
        :return:
        """
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if status == 0:
            print("output:", output)
            result = re.findall(ifname + r'.*?inet addr:.*?(\d+\.\d+\.\d+\.\d+)', output, re.S | re.I)
            if result:
                ip = result[0]
                return ip

    def test_proxy(self, proxy):
        try:
            response = requests.get(TEST_URL, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout=TEST_TIMEOUT)

            if response.status_code == 200:
                return True

        except Exception as error:
            print("test_proxy:", error)
            return False

    def remove_proxy(self):
        """
        移除代理
        :return: None
        """
        self.redis = RedisClient()
        self.redis.remove(CLIENT_NAME)
        print('Successfully Removed Proxy')

    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()

        if self.redis.set(CLIENT_NAME, proxy):
            print('Successfully Set Proxy', proxy)

    def exists_proxy(self):
        """
        代理是否存在
        :return: bool
        """
        self.redis = RedisClient()
        return self.redis.exists(CLIENT_NAME)

    def count_time_interval(self):
        return time.time() - self.timer

    def adsl(self):
        while True:
            print("ADSL Start,Remove Proxy,Please wait")
            try:
                self.remove_proxy()
            except:
                while True:
                    (status, output) = subprocess.getstatusoutput(ADSL_BASH)
                    if status == 0:
                        self.remove_proxy()
                        break
            # 从拨号到IP可用有一定时间间隔
            subprocess.getstatusoutput(ADSL_BASH_STOP)
            time.sleep(1)
            (status, output) = subprocess.getstatusoutput(ADSL_BASH_START)
            print('status:', status, '\noutput', output)

            if status == 0:
                print("ADSL successfully!")
                ip = self.get_ip()
                if ip:
                    print("Now IP:", ip)
                    print("Testing Proxy,Please wait!")
                    proxy = f'{ip}:{PROXY_PORT}'
                    data = {CLIENT_NAME: proxy}
                    if self.test_proxy(proxy):
                        print('Valid Proxy!')
                        # 接口方式在另一台服务器新增proxy
                        self.set_proxy(proxy)
                        time.sleep(ADSL_CYCLE)
                    else:
                        print('Invalid Proxy!')
                        print('Sleeping...')
                        subprocess.getstatusoutput('service tinyproxy stop')
                        time.sleep(1)
                        subprocess.getstatusoutput('service tinyproxy restart')
            else:
                print("Get IP Failed,Re dialing")


if __name__ == '__main__':
    sender = Sender()
    sender.adsl()

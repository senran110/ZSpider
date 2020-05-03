import time

from util.FastProxy import FastIpSpider


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        """
        判断方法是否以crawl_开头若是就将其加入__CrawlFunc__属性中
        :param name:
        :param bases:
        :param attrs:
        :return:
        """
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)  # 将方法名添加到 属性中
                count += 1

        attrs['__CrawlFuncCount__'] = count  # 方法数量
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def __init__(self):
        self.fast_ip = FastIpSpider()

    def get_proxies(self, callback):
        """
        获取代理
        :param callback: 抓取函数列表
        :return:
        """
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print(f'成功获取到代理{proxy}!')
            proxies.append(proxy)
        return proxies

    def crawl_FastIP(self, count=5):
        """
        抓取快代理
        :param count:
        :return:
        """
        for i in range(1, count):
            yield from self.fast_ip.parse_ip(i)
            time.sleep(1)

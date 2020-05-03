import sys

from util.redis_client import RedisClient
from ProxyGetter.crawler import Crawler
from util.GetConfig import cf

POOL_UPPER_THRESHOLD = int(cf.get("Pool", "POOL_UPPER_THRESHOLD"))


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()  # 实例化redis类
        self.crawler = Crawler()  # 实例化爬虫类

    def is_over_threshold(self):
        """
        判断代理数量是否达到限制
        :return:
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行...')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):

                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)

                sys.stdout.flush()  # 强制刷新缓冲区

                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    secs = cf.sections()
    INITIAL_SCORE = cf.get("Pool", "INITIAL_SCORE")

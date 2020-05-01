import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from zh.util.file_helper import get_cookie_from_txt


class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent):
        super(RandomUserAgent, self).__init__()
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent


class LoginMiddleware(object):
    def __init__(self):
        self.filename = "cookie.txt"

    def process_request(self, request, spider):
        if spider.name == 'zh':
            # print("添加cookie...")
            request.cookies = get_cookie_from_txt(self.filename)

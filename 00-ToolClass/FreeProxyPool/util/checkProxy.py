import time
import sys
import aiohttp
import asyncio

from util.redis_client import RedisClient
from util.GetConfig import cf

try:
    from aiohttp import ClientError
except Exception:
    from aiohttp import ClientProxyConnectionError

TEST_URL = cf.get("Pool", "TEST_URL")
BATCH_TEST_SIZE = int(cf.get("Pool", "BATCH_TEST_SIZE"))
VALID_STATUS_CODES = [200, 302]


class Tester(object):
    """
    异步 aiohttp  http请求， 需要配合 异步关键词async 使用
    """

    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = f'http://{proxy}'
                print(f'正在测试{proxy}')

                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print(f'代理可用{proxy}')
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法 ', response.status, 'IP', proxy)

            except (ClientError, aiohttp.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print(f'代理请求失败{proxy}')

    def run(self):
        """
        测试主函数
        :return:
        """
        try:
            count = self.redis.count()
            print(f'当前剩余{count}个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)

                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                # 注释sys.stdout.flush()只能等到程序执行完毕，屏幕会一次性输出// 刷新stdout,能看到实时输出信息
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)

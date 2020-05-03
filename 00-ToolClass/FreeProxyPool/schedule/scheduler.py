import time
from multiprocessing import Process

from util.checkProxy import Tester
from util.GetConfig import cf
from web_api.api import app
from ProxyGetter.getter import Getter

API_HOST = cf.get("API", "API_HOST")
API_PORT = int(cf.get("API", "API_PORT"))
TESTER_CYCLE = int(cf.get("Pool", "TESTER_CYCLE"))
GETTER_CYCLE = int(cf.get("Pool", "GETTER_CYCLE"))
TESTER_ENABLED = cf.get("Func", "TESTER_ENABLED")
GETTER_ENABLED = cf.get("Func", "GETTER_ENABLED")
API_ENABLED = cf.get("Func", "API_ENABLED")


class Schedule:
    def __init__(self):
        # self.LogHandler = myLogHandler("pool")
        pass

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            # self.LogHandler.log('测试器开始运行...')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            # self.LogHandler.log('开始抓取代理...')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        print(API_HOST,API_PORT)
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行...')

        if TESTER_ENABLED:  # 检测模块
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:  # 获取模块
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:  # webAPI模块
            api_process = Process(target=self.schedule_api)
            api_process.start()

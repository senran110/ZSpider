"""
@file:config.py
@time:2019/9/18-10:47
"""
# 拨号网卡
ADSL_IFNAME = 'ppp0'
# 测试超时时间
TEST_TIMEOUT = 5
# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 5
# 拨号间隔
ADSL_CYCLE = 120
# ADSL命令
ADSL_BASH_STOP = 'pppoe-stop'
ADSL_BASH_START = 'pppoe-start'
# 代理端口
PROXY_PORT = 8888
# 测试网址
TEST_URL = "http://icanhazip.com"
CLIENT_NAME = "adsl1"

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWD = None

PROXY_KEY = "adslproxy"

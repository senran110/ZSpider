# -*- coding: utf-8 -*-

BOT_NAME = 'zh'

SPIDER_MODULES = ['zh.spiders']
NEWSPIDER_MODULE = 'zh.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'zh (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "zh.middlewares.RandomUserAgent": 543,
    "zh.middlewares.LoginMiddleware": 542
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'zh.pipelines.ZhPipeline': 300,
}

MY_USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Linux; Android 7.0; EVA-L09) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36'
]

# 确保request存储到redis中
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 确保所有爬虫共享相同的去重指纹
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 在redis中保持scrapy-redis用到的队列，不会清除redis中的队列，从而实现暂停和恢复的功能
SCHEDULER_PERSIST = True

# REDIS_HOST = '47.100.139.162'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_ENCODING = "utf-8"

#  設置mysql存儲
MYSQL_HOST = '47.100.139.162'
MYSQL_DBNAME = 'zh_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = 3306

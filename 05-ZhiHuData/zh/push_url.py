"""
@file:push_url.py
@time:2020/2/17-21:10
"""
import redis

redis_conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
redis_conn.lpush('DD:start_urls', 'http://category.dangdang.com/')
# redis_conn.lpush('zh:start_urls', 'https://www.zhihu.com/hot?list=science')

print("插入成功....")

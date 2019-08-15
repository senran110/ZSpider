"""
@file:fontcache.py
@time:2019/8/10-10:37
"""
import redis


class Cache:
    def __init__(self, redis_host='127.0.0.1', redis_port=6379, redis_pass=None):
        if redis_pass:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.HASH_TABLE = "DP:FONT"

    def add_hash(self, name, json_data):
        """新增hash
        """
        self.r.hset(self.HASH_TABLE, name, json_data)

    def check_hash(self, name):
        """判断 hash key 是否存在
        """
        return self.r.hexists(self.HASH_TABLE, name)

    def get_hash(self, name):
        return self.r.hget(self.HASH_TABLE, name)

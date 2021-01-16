# coding=utf-8
# Author: huxin
# Time : 2020/9/17:15:08
import redis
import json


class Redis:

    @staticmethod
    def get_connect(redis_info):
        r = redis.Redis(host=redis_info["host"], port=redis_info["port"], db=redis_info["db"], password=redis_info["password"])
        return r

    @staticmethod
    def get_value(redis_info,name,key) -> dict:
        """
        name:redis中的HASH
        key:HASH下面的key值
        """
        r = Redis().get_connect(redis_info)
        value = r.hget(name,key)
        value = json.loads(value)
        return value



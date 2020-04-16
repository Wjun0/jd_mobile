import redis
import requests
import hashlib
import pickle
from redis import StrictRedis

# 1,对要去重的请求进行hash
# 2,将hash保存到redis
# 3,判断hash是否在redis中

class Redis_filter(object):
    def __init__(self):
        self.redis_list = []
        self.redis_con = StrictRedis(host='192.168.59.128', port='6379')

    def _get_hash(self, data):
        md5 = hashlib.md5()
        hs = pickle.dumps(data)
        md5.update(hs)
        return md5.hexdigest()

    def save(self, data):
        hash_data = self._get_hash(data)
        self.redis_con.lpush("filter_key", hash_data)

    def get(self, data):
        hash_data = self._get_hash(data)
        lis = self.redis_con.lrange('filter_key', 0, -1)
        lis = [i.decode() for i in lis]
        if hash_data in lis:
            return True
        return False

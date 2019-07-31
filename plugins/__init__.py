import json
import redis
from plugins.dispatch import *


pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
m_redis = redis.Redis(connection_pool=pool)


class MRedis:
    @classmethod
    def set_json(cls, key, data):
        assert isinstance(data, (dict, list)), '请传递字符串，字典，集合类型的数据'
        m_redis.set(key, json.dumps(data, ensure_ascii=False))

    @classmethod
    def get_json(cls, key):
        v = m_redis.get(key)
        return json.loads(v) if v else None




import redis

from config import settings


class RedisTools:

    __redis_connect = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    @classmethod
    def set_pair(cls, key: str, value: str):
        cls.__redis_connect.set(key, value)

    @classmethod
    def get_pair(cls, pair: str):
        return cls.__redis_connect.get(pair)


redis_tools = RedisTools()


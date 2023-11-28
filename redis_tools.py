import redis
from redis import asyncio as aioredis

from config import settings


class RedisTools:
    async_redis = aioredis.from_url(settings.redis_url, encoding='utf-8', decode_responses=True)
    # __redis_connect = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    @classmethod
    async def set_pair(cls, key: str, value: str, expiry: int):
        await cls.async_redis.set(key, value, expiry)

    @classmethod
    async def get_pair(cls, pair: str):
        return await cls.async_redis.get(pair)


redis_tools = RedisTools()


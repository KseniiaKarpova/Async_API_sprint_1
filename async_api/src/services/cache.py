import json
from redis.asyncio import Redis


class RedisCache:
    CACHE_EXPIRE_IN_SECONDS = 300

    def __init__(self, redis: Redis, expire: int = None):
        self.redis = redis
        self.expire = expire or RedisCache.CACHE_EXPIRE_IN_SECONDS

    async def get_from_cache(self, url: str):
        result = await self.redis.get(
            str(url),
        )
        if result:
            result = json.loads(result)
        return result

    async def put_to_cache(self, url: str, data):
        data = json.dumps(data)
        await self.redis.setex(name=str(url), value=data, time=self.expire)

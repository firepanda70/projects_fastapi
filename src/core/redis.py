from datetime import timedelta

from redis.asyncio import Redis

from .schemas import CustomSchema
from .config import config, REDIS_EXPIRE


class RedisData(CustomSchema):
    key: bytes | str
    value: bytes | str
    ttl: int | timedelta | None = REDIS_EXPIRE


class RedisClient:
    def __init__(self, url: str) -> None:
        self.client = Redis.from_url(url)

    async def set_data(self, redis_data: RedisData, *, is_transaction: bool = False) -> None:
        async with self.client.pipeline(transaction=is_transaction) as pipe:
            await pipe.set(redis_data.key, redis_data.value, ex=redis_data.ttl)
            await pipe.execute()

    async def get(self, key: str, ex: int | timedelta | None = REDIS_EXPIRE) -> str | None:
        return await self.client.getex(key, ex)

    async def delete(self, key: str) -> None:
        return await self.client.delete(key)


redis_client = RedisClient(str(config.redis))

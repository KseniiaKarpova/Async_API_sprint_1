from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis
from services.cache import RedisCache

from fastapi import Depends


class GenreStorage:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_data_list(self):
        try:
            doc = await self.elastic.search(index="genres")
            hits = doc['hits']['hits']
            genres = [hit['_source'] for hit in hits]
            return genres
        except NotFoundError:
            return None

    async def get_data_by_id(self, id: UUID) -> dict:
        try:
            doc = await self.elastic.get(index="genres", id=id)
        except NotFoundError:
            return None
        return doc["_source"]


class GenreService:
    def __init__(self, cache: RedisCache, storage: GenreStorage):
        self.cache = cache
        self.storage = storage

    async def get_data_by_id(self, url: str, id: UUID) -> dict:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_data_list(self, url: str) -> list[dict]:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_list()
            if data:
                await self.cache.put_to_cache(url, data)
        return data


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    redis = RedisCache(redis)
    elastic = GenreStorage(elastic)
    return GenreService(redis, elastic)

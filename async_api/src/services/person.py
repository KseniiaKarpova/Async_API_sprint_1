from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis
from services.cache import RedisCache

from fastapi import Depends


class PersonStorage:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_data_by_id(self, id: UUID) -> dict:
        try:
            doc = await self.elastic.get(index="persons", id=id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def search_data(self, query, page_number, page_size):
        search_query = {"query_string": {"default_field": "name", "query": query}}
        docs = await self.elastic.search(
            index="persons",
            body={
                "_source": ["id", "name", "films"],
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]

    async def get_film(self, id: UUID):
        try:
            filter_query = ({
                "bool": {
                    "should": [{
                        "nested": {
                            "path": "actors",
                            "query": {"bool": {"must": {"match": {"actors.id": id}}}},
                        }},
                        {"nested": {
                            "path": "writers",
                            "query": {"bool": {"must": {"match": {"writers.id": id}}}},
                        }}
                    ]
                }
            })
            docs = await self.elastic.search(
                index="movies",
                body={
                    "_source": ["id", "title", "imdb_rating", 'actors', 'writers'],
                    "query": filter_query,
                },
                params={"filter_path": "hits.hits._source"},
            )
            if not docs:
                return None
            return [film["_source"] for film in docs["hits"]["hits"]]
        except NotFoundError:
            return None


class PersonService:
    def __init__(self, cache: RedisCache, storage: PersonStorage):
        self.cache = cache
        self.storage = storage

    async def search_data(self, url: str, query, page_number: int, page_size: int):
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.search_data(query, page_number=page_number, page_size=page_size)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_data_by_id(self, url: str, id: UUID) -> dict:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_film(self, url: str, id: UUID) -> list[dict]:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_film(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    redis = RedisCache(redis)
    elastic = PersonStorage(elastic)
    return PersonService(redis, elastic)

from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis
from services.cache import RedisCache

from fastapi import Depends


class FilmStorage:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def search_data(self, query, page_number, page_size):
        search_query = {"query_string": {"default_field": "title", "query": query}}
        docs = await self.elastic.search(
            index="movies",
            body={
                "_source": ["id", "title", "imdb_rating"],
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]

    async def get_data_by_id(self, id: UUID) -> dict:
        try:
            doc = await self.elastic.get(index="movies", id=id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def get_data_list(
        self, sort: str, genre: UUID, page_number: int, page_size: int
    ) -> list[dict] | None:
        if sort[0] == "-":
            sort = {sort[1:]: "desc"}
        else:
            sort = {sort: "asc"}
        filter_query = (
            {"match_all": {}}
            if genre is None
            else {
                "nested": {
                    "path": "genre",
                    "query": {"bool": {"must": {"match": {"genre.id": genre}}}},
                }
            }
        )
        docs = await self.elastic.search(
            index="movies",
            body={
                "_source": ["id", "title", "imdb_rating"],
                "sort": sort,
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": filter_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]


class FilmService:
    def __init__(self, cache: RedisCache, storage: FilmStorage):
        self.cache = cache
        self.storage = storage

    async def search_data(self, query, page_number: int, page_size: int):
        data = await self.storage.search_data(query, page_number=page_number, page_size=page_size)
        return data

    async def get_data_by_id(self, url: str, id: UUID) -> dict:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_data_list(
        self, sort: str, genre: UUID, page_number: int, page_size: int
    ) -> list[dict]:
        data = await self.storage.get_data_list(
            sort=sort, genre=genre, page_number=page_number, page_size=page_size
        )
        return data


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    redis = RedisCache(redis)
    elastic = FilmStorage(elastic)
    return FilmService(redis, elastic)

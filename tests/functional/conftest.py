import pytest
import asyncio
import aiohttp
from elasticsearch import AsyncElasticsearch
from functional.settings import test_settings, movies_mappings
from elasticsearch.helpers import async_bulk
import uuid


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(name='es_write_data')
def es_write_data():
    async def inner(data: list[dict]):
        es_url = f"http://{test_settings.es_host}:{test_settings.es_port}"
        es_client = AsyncElasticsearch(hosts=es_url, verify_certs=False)
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **movies_mappings)

        updated, errors = await async_bulk(client=es_client, actions=data)

        await es_client.close()

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture(name='make_get_request')
def make_get_request():
    async def inner(endpoint, params):
        session = aiohttp.ClientSession()
        url = f"{test_settings.service_url}{endpoint}"
        async with session.get(url, params=params) as response:
            json, status = await response.json(), response.status
        await session.close()
        return json, status
    return inner


@pytest.fixture(name='es_data', scope='session')
def es_data():
    data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
            {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
        ],
        'writers': [
            {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
            {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
        ],
    } for _ in range(60)]
    bulk_query: list[dict] = []
    for row in data:
        data = {'_index': 'movies', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)
    return bulk_query
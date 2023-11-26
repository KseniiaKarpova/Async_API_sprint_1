import uuid

import aiohttp
import pytest
from functional.conftest import es_write_data, es_data, make_get_request
from functional.settings import test_settings

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий. 

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star', 'page_number': 1, 'page_size': 50},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato', 'page_number': 1, 'page_size': 1},
                {'status': 404, 'length': 1}
        )
    ]
)

@pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, es_data: list[dict] ,query_data, expected_answer):  
    await es_write_data(es_data)

    session = aiohttp.ClientSession()
    
    # 3. Запрашиваем данные из ES по API
    import time
    time.sleep(10)
    body, status = await make_get_request(endpoint='/api/v1/films/search', params=query_data)

    # 4. Проверяем ответ 

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']

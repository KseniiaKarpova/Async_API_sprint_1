from logging import config as logging_config

from core.logger import LOGGING

from fastapi import Query
from pydantic_settings import BaseSettings
from pydantic import Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class QueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


class Settings(BaseSettings):
    project_name: str = Field('Async API', env='PROJECT_NAME')
    redis_port: int = Field('http://app:8000', env='REDIS_PORT')
    es_host: str = Field('elasticsearch', env='ES_HOST')
    es_port: str = Field('9200', env='ES_PORT')
    redis_host: str = Field('cache', env='REDIS_HOST')

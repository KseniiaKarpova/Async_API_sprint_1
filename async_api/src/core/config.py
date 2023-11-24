import os
from logging import config as logging_config

from core.logger import LOGGING

from fastapi import Query
from pydantic_settings import BaseSettings
from pydantic import Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    elastic_host: str = Field('elasticsearch', env='ES_HOST')
    elastic_port: str = Field('9200', env='ES_PORT')
    redis_host: str = Field('cache', env='REDIS_HOST')

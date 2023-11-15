import uuid
from typing import Union

import orjson
from models import orjson_dumps
from pydantic import BaseModel


class BaseModelOrjson(BaseModel):
    id: uuid.UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModelOrjson):
    title: str
    imdb_rating: float


class FilmDetail(BaseModelOrjson):
    title: str
    imdb_rating: Union[float, None] = None
    genre: list
    title: str
    description: str | None
    director: list | None
    actors: list = None
    writers: list = None

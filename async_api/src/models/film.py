import uuid
from typing import List, Optional, Union

import orjson
from models import orjson_dumps
from models.person import Person
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
    imdb_rating: float = None
    genre: list
    title: str
    description: str = None
    director: list = None
    actors: list = None
    writers: list = None

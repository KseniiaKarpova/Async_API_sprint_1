import uuid
from typing import List, Union

import orjson
from models import orjson_dumps
from models.person import Person
from models.genre import Genre
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
    imdb_rating: float
    description: str | None
    genre: list[dict | None]
    actors: list[dict | None]
    writers: list[dict | None]
    director: list[str | None]


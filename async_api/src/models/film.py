import uuid
from typing import List, Union, Optional, Dict

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
    imdb_rating: Union[float, None] = None
    genre: List
    title: str
    description: str
    director: List | None
    actors_names:  Optional[List] = None
    writers_names: Optional[List] = None
    actors: List[Person]
    writers: List[Person]
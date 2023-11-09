import uuid
from typing import List, Union

import orjson
from models import orjson_dumps
from models.person import Person
from models.genre import Genre
from pydantic import BaseModel


class Film(BaseModel):
    id: uuid.UUID
    imdb_rating: Union[float, None] = None
    genre: List[Genre | None]
    title: str | None
    description: str | None
    director: List[Person | None]
    actors: List[Person | None]
    writers: List[Person | None]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

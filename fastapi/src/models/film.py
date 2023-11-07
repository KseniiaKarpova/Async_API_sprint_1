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
    genre: List[Genre]
    title: str
    description: str
    director: str
    actors_names: str
    writers_names: str
    actors: List[Person]
    writers: List[Person]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps

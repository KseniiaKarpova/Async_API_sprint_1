import uuid
from typing import List, Optional, Union
from models.base import Base0rjsonModel


class BaseModelOrjson(Base0rjsonModel):
    id: uuid.UUID


class Film(BaseModelOrjson):
    title: str
    imdb_rating: float


class FilmDetail(BaseModelOrjson):
    title: str
    imdb_rating: Union[float, None] = None
    genre: List
    title: str
    description: str | None
    director: list | None
    actors: Optional[List] = None
    writers: Optional[List] = None

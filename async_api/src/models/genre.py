import uuid

import orjson
from models import orjson_dumps
from pydantic import BaseModel


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: str

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps

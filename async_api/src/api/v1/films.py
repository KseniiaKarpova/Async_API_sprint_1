from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from models.film import Film
from core.config import QueryParams

from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    "",
    response_model=List[Film],
    response_description="Example of films.",
    response_model_exclude={"description", "genre", "actors", "writers", "director"},
    summary="List films",
    description="List films with pagination, "
                "genre filtration, film and rate sorting.",
)
async def get_film_list(
        film_service: FilmService = Depends(get_film_service),
        sort: str = "-imdb_rating",
        genre: Optional[UUID] = None,
        commons: QueryParams = Depends(QueryParams),
) -> List[Film]:
    films = await film_service.get_data_list(sort, genre, commons.page_number, commons.page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return [
        Film(
            id=film["id"],
            title=film["title"],
            imdb_rating=film["imdb_rating"],
        )
        for film in films
    ]


from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from core.config import QueryParams
from models.film import Film, FilmDetail
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter()


@router.get(
    "",
    response_model=List[Film],
    response_description="Example of films",
    response_model_exclude={"description", "genre", "actors", "writers", "director"},
    summary="List films",
    description="List films with pagination, "
                "genre filtration, film and rate sorting.",
)
async def get_film_list(
        film_service: FilmService = Depends(get_film_service),
        sort: str = "-imdb_rating",
        genre: UUID | None = None,
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


@router.get(
    "/search",
    response_model=List[Film],
    response_description="Example of films",
    response_model_exclude={"description", "genre", "actors", "writers", "director", "actors_names", "writers_names"},
    description="Film searching",
    summary="List of films",
)
async def search_films(
    film_service: FilmService = Depends(get_film_service),
    query: str = "",
    commons: QueryParams = Depends(QueryParams),
) -> Optional[List[Dict[str, Film]]]:
    films = await film_service.search_data(query, commons.page_number, commons.page_size)
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


@router.get(
    "/{uuid}",
    response_model=FilmDetail,
    response_model_exclude={"actors_names", "writers_names"},
    response_description="Example of film",
    summary="Film",
    description="Getting film by id",
)
async def get_film_details(
    request: Request, film_id: UUID, film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_data_by_id(url=str(request.url), id=str(film_id))
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film Not Found")
    return FilmDetail(
        id=film["id"],
        title=film["title"],
        imdb_rating=film["imdb_rating"],
        description=film["description"],
        genre=film["genre"],
        actors=film["actors_names"],
        writers=film["writers_names"],
        director=film["director"],
    )

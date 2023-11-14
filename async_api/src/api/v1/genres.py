from http import HTTPStatus
from typing import List
from uuid import UUID

from models.genre import Genre
from services.genres import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter()


@router.get(
    "/",
    response_model=list[Genre],
    response_description="Example of genres",
    summary="List of genres",
)
async def get_genres(
    request: Request,
    service: GenreService = Depends(get_genre_service)
) -> List[Genre]:
    genres = await service.get_data_list(url=str(request.url))
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres Not Found")
    return [Genre(**genre) for genre in genres]


@router.get(
    "/{uuid}",
    response_model=Genre,
    response_description="Example of genre",
    summary="Genre",
    description="Getting genre by uuid",
)
async def get_genre_by_id(
        request: Request,
        uuid: UUID,
        service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await service.get_data_by_id(url=str(request.url), id=str(uuid))
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre Not Found")
    return Genre(**genre)

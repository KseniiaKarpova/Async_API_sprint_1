from http import HTTPStatus
from uuid import UUID

from core.config import QueryParams
from models.film import Film
from models.person import Person, PersonDetails
from services.person import PersonService, get_person_service

from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter()


@router.get(
    "/search",
    response_model=list[PersonDetails],
    response_description="Example of person",
    description="Person searching",
    summary="List of person",
)
async def search_person(
    request: Request,
    service: PersonService = Depends(get_person_service),
    query: str = "",
    commons: QueryParams = Depends(QueryParams),
) -> list[dict[str, Person]]:
    persons = await service.search_data(url=str(request.url),
                                        query=query,
                                        page_number=commons.page_number,
                                        page_size=commons.page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person Not Found")
    return [PersonDetails(**person) for person in persons]


@router.get(
    "/{uuid}",
    response_model=PersonDetails,
    response_description="Example of person",
    summary="Person",
    description="Getting person by uuid",
)
async def get_person_by_id(
        request: Request,
        uuid: UUID,
        service: PersonService = Depends(get_person_service)
) -> Person:
    person = await service.get_data_by_id(url=str(request.url), id=str(uuid))
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person Not Found")
    return PersonDetails(**person)


@router.get(
    "/{uuid}/film",
    response_model=list[Film],
    response_description="Example of person",
    summary="Person",
    description="Getting person by uuid",
)
async def get_films_by_person(
    request: Request,
    uuid: UUID,
    service: PersonService = Depends(get_person_service)
) -> list[dict[str, Film]]:
    films = await service.get_film(url=str(request.url), id=str(uuid))
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return films
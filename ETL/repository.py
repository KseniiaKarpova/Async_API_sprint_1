from typing import Any
from sqlalchemy import select, func, case
from db.schemas import FilmWork, Person, Genre, GenreFilmwork, PersonFilmWork
from abc import abstractmethod


class BaseRepository:
    table = None

    @classmethod
    def get_many(cls, attribute: str, value: Any, session, offset):
        """
        SELECT from cls.table by specified attribute. Return many objects
        """
        with session:
            instances = (session.execute(
                select(cls.table).where(getattr(cls.table, attribute) == value).offset(offset=offset)
            )).scalars()
        return instances

    @abstractmethod
    def last_updateds(limit, offset, updated_at):
        ...


class PersonRepository(BaseRepository):
    table = Person

    @staticmethod
    def last_updateds(limit, offset, updated_at):
        return select(
                Person.id,
                Person.full_name.label('name'),
            ).where(
                Person.modified>updated_at
                ).order_by(Person.modified).limit(limit).offset(offset)

    @staticmethod
    def film_persons_name_subquery(role, label):
        subquery = (
            select(FilmWork.id, func.array_agg(Person.full_name).label(label)).where(
                PersonFilmWork.role==role
            )
            .join(PersonFilmWork, FilmWork.id == PersonFilmWork.film_work_id)
            .join(Person, Person.id == PersonFilmWork.person_id)
            .group_by(FilmWork.id)
            .alias(label)
        )

        return subquery

    @staticmethod
    def film_persons_subquery(role, label):
        subquery = (
            select(FilmWork.id, 
                   func.array_agg(
                       func.json_build_object(
                           'id', Person.id,
                           'name', Person.full_name,
                   )).label(label)).where(
                PersonFilmWork.role==role
            )
            .join(PersonFilmWork, FilmWork.id == PersonFilmWork.film_work_id)
            .join(Person, Person.id == PersonFilmWork.person_id)
            .group_by(FilmWork.id)
            .alias(label)
        )

        return subquery



class FilmWorkRepository(BaseRepository):
    table = FilmWork
    
    @staticmethod
    def all():
        query = select(func.count(FilmWork.id))
        return query

    @staticmethod
    def last_updateds(limit, offset, updated_at):
        genre_subquery = (
            select(FilmWork.id, func.array_agg(Genre.name).label('genre'))
            .join(GenreFilmwork, GenreFilmwork.film_work_id == FilmWork.id)
            .join(Genre, GenreFilmwork.genre_id == Genre.id)
            .group_by(FilmWork.id)
            .alias('genre')
        )
        actors_names_subquery = PersonRepository.film_persons_name_subquery(role='actor', label='actors_names')
        actors_subquery = PersonRepository.film_persons_subquery(role='actor', label='actors')
        director_subquery = PersonRepository.film_persons_name_subquery(role='director', label='director')
        writers_names_subquery = PersonRepository.film_persons_name_subquery(role='writer', label='writers_names')
        writers_subquery = PersonRepository.film_persons_subquery(role='writer', label='writers')
        query = select(
            FilmWork.id,
            FilmWork.rating.label('imdb_rating'),
            FilmWork.title,
            FilmWork.description,
            FilmWork.modified,
            case(
                (genre_subquery.c.genre.isnot(None), genre_subquery.c.genre),
                (True, [])  # Default case for an empty list
            ).label('genre'),

            case(
                (actors_names_subquery.c.actors_names.isnot(None), actors_names_subquery.c.actors_names),
                (True, [])  # Default case for an empty list
            ).label('actors_names'),

            case(
                (actors_subquery.c.actors.isnot(None), actors_subquery.c.actors),
                (True, [])  # Default case for an empty list
            ).label('actors'),

            case(
                (director_subquery.c.director.isnot(None), director_subquery.c.director),
                (True, [])  # Default case for an empty list
            ).label('director'),

            case(
                (writers_subquery.c.writers.isnot(None), writers_subquery.c.writers),
                (True, [])  # Default case for an empty list
            ).label('writers'),

            case(
                (writers_names_subquery.c.writers_names.isnot(None), writers_names_subquery.c.writers_names),
                (True, [])  # Default case for an empty list
            ).label('writers_names'),
            ).outerjoin(
                genre_subquery, FilmWork.id == genre_subquery.c.id,
                ).outerjoin(
                    actors_names_subquery, FilmWork.id == actors_names_subquery.c.id).outerjoin(
                        actors_subquery, FilmWork.id == actors_subquery.c.id).outerjoin(
                            director_subquery, FilmWork.id == director_subquery.c.id).outerjoin(
                                writers_subquery, FilmWork.id == writers_subquery.c.id).outerjoin(
                                    writers_names_subquery, FilmWork.id == writers_names_subquery.c.id
                            ).where(
                                FilmWork.modified>updated_at
                                ).order_by(FilmWork.modified).limit(limit).offset(offset)
        return query


class GenreRepository(BaseRepository):
    table = Genre

    @staticmethod
    def last_updateds(limit, offset, updated_at):
        return select(
                Genre.id,
                Genre.name,
                Genre.description,
            ).where(
                Genre.modified>updated_at
                ).order_by(Genre.modified).limit(limit).offset(offset)
        

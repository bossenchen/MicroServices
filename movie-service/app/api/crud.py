from .models import MovieIn
from .db import movies, database


async def add_movie(payload: MovieIn):
    query = movies.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_movies():
    query = movies.select()
    return await database.fetch_all(query=query)


async def get_movie(movie_id: int):
    query = movies.select(movies.c.id == movie_id)
    return await database.fetch_one(query=query)


async def delete_movie(movie_id: int):
    query = movies.delete().where(movies.c.id == movie_id)
    return await database.execute(query=query)


async def update_movie(movie_id: int, payload: MovieIn):
    query = movies.update().where(movies.c.id == movie_id).values(**payload.dict())
    return await database.execute(query=query)

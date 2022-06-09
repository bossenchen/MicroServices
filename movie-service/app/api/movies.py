from typing import List

from fastapi import APIRouter, HTTPException

from . import crud
from .models import MovieOut, MovieIn, MovieUpdate
from .service import is_cast_present, get_casts_service_host

movies = APIRouter()


@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id {cast_id} not found")

    movie_id = await crud.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }

    return response


@movies.get('/', response_model=List[MovieOut])
async def get_movies():
    return await crud.get_all_movies()


@movies.get('/{movie_id}', response_model=MovieOut)
async def get_movie(movie_id: int):
    movie = await crud.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies.put('/{movie_id}', response_model=MovieOut)
async def update_movie(movie_id: int, payload: MovieUpdate):
    movie = await crud.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)

    return await crud.update_movie(movie_id, updated_movie)


@movies.delete('/{movie_id}', response_model=MovieOut)
async def delete_movie(movie_id: int):
    movie = await crud.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await crud.delete_movie(movie_id)

    return movie


@movies.get('/casts_service_host')
async def get_host():
    return get_casts_service_host()

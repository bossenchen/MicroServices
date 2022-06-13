from typing import List

from fastapi import APIRouter, HTTPException

from . import crud
from .models import CastOut, CastIn, CastUpdate

casts = APIRouter()


@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await crud.add_cast(payload)

    response = {
        'id': cast_id,
        **payload.dict()
    }

    return response


@casts.get('/{cast_id}', response_model=CastOut)
async def get_cast(cast_id: int):
    cast = await crud.get_cast(cast_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast


@casts.put('/{cast_id}', response_model=CastOut)
async def update_cast(cast_id: int, payload: CastUpdate):
    cast = await crud.get_cast(cast_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")

    update_data = payload.dict(exclude_unset=True)
    cast_in_db = CastIn(**cast)
    updated_cast = cast_in_db.copy(update=update_data)

    await crud.update_cast(cast_id, updated_cast)
    return updated_cast


@casts.delete('/{cast_id}', response_model=CastOut)
async def delete_casts(cast_id: int):
    cast = await crud.get_cast(cast_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    await crud.delete_cast(cast_id)
    return cast


@casts.get('/', response_model=List[CastOut])
async def get_casts():
    return await crud.get_all_casts()

from .models import CastIn
from .db import casts, database


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_cast(cast_id: int):
    query = casts.select(casts.c.id == cast_id)
    return await database.fetch_one(query=query)


async def delete_cast(cast_id: int):
    query = casts.delete().where(casts.c.id == cast_id)
    return await database.execute(query=query)


async def get_all_casts():
    query = casts.select()
    return await database.fetch_all(query=query)

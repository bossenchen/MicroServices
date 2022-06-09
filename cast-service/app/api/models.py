from typing import Optional

from pydantic import BaseModel, PositiveInt


class CastIn(BaseModel):
    name: str
    nationality: Optional[str] = None


class CastOut(CastIn):
    id: PositiveInt


class CastUpdate(CastIn):
    name: Optional[str] = None

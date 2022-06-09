from typing import List, Optional

from pydantic import BaseModel, PositiveInt


class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts_id: List[int]


class MovieOut(MovieIn):
    id: PositiveInt


class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts_id: Optional[List[int]] = None

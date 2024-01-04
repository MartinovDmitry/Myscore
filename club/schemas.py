import datetime
from typing import Optional

from pydantic import BaseModel


class SchClubCreate(BaseModel):
    title: str
    description: str
    date_of_foundation: datetime.date
    location: str
    players_quantity: int
    stuff_quantity: int
    coach_name: str
    coach_id: Optional[int | None] = None
    league_name: str
    league_id: int
    rating: int


class SchClubResponse(SchClubCreate):
    pass

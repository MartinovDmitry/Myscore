from typing import Optional

from pydantic import BaseModel


class SchLeagueBase(BaseModel):
    league_name: str
    country: str
    clubs_number: int


class SchLeagueCreate(SchLeagueBase):
    pass


class SchLeagueResponse(SchLeagueBase):
    pass


class SchLeagueUpdated(SchLeagueBase):
    league_name: str
    country: Optional[str | None] = None
    clubs_number: Optional[int | None] = None

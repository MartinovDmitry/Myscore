from typing import Optional

from pydantic import BaseModel


class SchStandingsResponse(BaseModel):
    name: str
    total_matches: Optional[int] = None
    record: str
    points: Optional[int] = None

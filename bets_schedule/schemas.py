from datetime import datetime

from pydantic import BaseModel


class SchScheduleResponse(BaseModel):
    event_name: str
    league_name: str
    date_event: datetime
    home_team: str
    away_team: str
    event_location: str


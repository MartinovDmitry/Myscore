from pydantic import BaseModel


class SchResponseConferenceInfo(BaseModel):
    name: str


class SchResponseTeamInfo(BaseModel):
    name: str
    abbreviation: str
    record: str
    conference: SchResponseConferenceInfo


class SchResponseScheduleInfo(BaseModel):
    league_name: str
    season_type: str
    event_name: str
    home_team: str
    away_team: str
    event_location: str


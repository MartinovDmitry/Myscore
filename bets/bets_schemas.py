from pydantic import BaseModel, Field


# for get_events_for_sport() func
class SchScore(BaseModel):
    event_status: str
    score_away: int
    score_home: int
    venue_name: str


class SchTeamsNormalized(BaseModel):
    team_id: int
    name: str
    record: str


class SchSchedule(BaseModel):
    league_name: str
    season_type: str
    event_name: str


class SchEventsResponse(BaseModel):
    sport_id: int
    score: SchScore
    teams_normalized: list[SchTeamsNormalized]
    schedule: SchSchedule
    lines: dict

from pydantic import BaseModel


class SchResponseConferenceInfo(BaseModel):
    name: str


class SchResponseTeamInfo(BaseModel):
    """
    for get_main_data_about_team() func
    """
    team_id: int
    name: str
    abbreviation: str
    record: str
    conference: SchResponseConferenceInfo


class SchResponseScheduleInfo(BaseModel):
    """
    for get_schedule_of_team() func
    """
    league_name: str
    season_type: str
    event_name: str
    home_team: str
    away_team: str
    event_location: str


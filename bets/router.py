from datetime import datetime
from typing import Optional

import requests
from fastapi import APIRouter, Path, Query

from bets.bets_schemas import SchEventsResponse
from bets.data_schemas import SchResponseTeamInfo, SchResponseScheduleInfo
from bets.view import get_main_data_about_team_view, get_schedule_of_team_view, get_events_for_sport_view

router = APIRouter(
    prefix='/bets',
    tags=['Bets'],
)

base_url = "https://therundown-inc.api.blobr.app/free-trial/"
sports_headers = {
  "X-BLOBR-KEY": "aKO5IueHAFFu5TZv8xJomNXu6GQsaZ1T"
}


@router.get('/sports')
async def get_sports():
    """
    Endpoint for getting all kinds of sports
    """
    sports_part = "v1/sports"
    response = requests.get(url=base_url + sports_part, headers=sports_headers)
    return response.json().get('sports')


@router.get('/sports/{sport_id}/team')
async def get_main_data_about_team(
        team_title: str = Query(default='Real Madrid'),
        sport_id: int = Path(),
) -> SchResponseTeamInfo | None:
    """
    Endpoint for getting team by title in chosen sport by id
    :param team_title: The title of required team
    :param sport_id: ID for spain Premier League (14)
    :return: Required team or None, if your title is invalid
    """
    result = await get_main_data_about_team_view(
        team_title=team_title,
        sport_id=sport_id,
    )
    return result


@router.get('/sports/{sport_id}/schedule')
async def get_schedule_of_team(
        team_title: str = Query(default='Real Madrid'),
        limit: int = Optional[Query()],
        sport_id: int = Path(),
) -> list[SchResponseScheduleInfo]:
    """
    Endpoint for getting team's schedule by title in chosen sport by id
    :param team_title: The title of team for schedule
    :param limit: optional param for limit
    :param sport_id: ID for spain Premier League (14)
    :return: Schedule for team by title
    """
    result = await get_schedule_of_team_view(
        team_title=team_title,
        limit=limit,
        sport_id=sport_id,
    )
    return result


@router.get('/sports/{sport_id}/events/{date}')
async def get_events_for_sport(
        sport_id: int,
        date: str,
) -> list[SchEventsResponse]:
    result = await get_events_for_sport_view(
        sport_id=sport_id,
        date=date,
    )
    return result

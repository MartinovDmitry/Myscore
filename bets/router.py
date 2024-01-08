from typing import Optional

import requests
from fastapi import APIRouter, Path, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bets.bets_schemas import SchEventsResponse
from bets.view import (get_and_record_in_db_main_data_about_team_view,
                       get_and_record_in_db_schedule_of_team_view,
                       get_events_for_sport_view,
                       place_a_bet_view)
from db_helper import session_factory

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
async def get_and_record_in_db_main_data_about_team(
        sport_id: int = Path(),
        session: AsyncSession = Depends(session_factory),
):
    result = await get_and_record_in_db_main_data_about_team_view(
        sport_id=sport_id,
        session=session,
    )
    return result


@router.get('/sports/{sport_id}/schedule')
async def get_and_record_in_db_schedule_of_team(
        team_title: str = Query(default='Real Madrid'),
        limit: int = Optional[Query()],
        sport_id: int = Path(),
        session: AsyncSession = Depends(session_factory),
):
    result = await get_and_record_in_db_schedule_of_team_view(
        team_title=team_title,
        limit=limit,
        sport_id=sport_id,
        session=session,
    )
    return result


@router.get('/sports/{sport_id}/events/{date}')
async def get_events_for_sport(
        sport_id: int,
        date: str,
) -> list[SchEventsResponse]:
    """
    Endpoint for getting main info about event with bets in desired date
    :param sport_id: ID for spain Premier League (14)
    :param date: Desired date
    :return: Main Info about event with bets
    """
    result = await get_events_for_sport_view(
        sport_id=sport_id,
        date=date,
    )
    return result


@router.post('/bets/events')
async def place_a_bet(
        sport_id: int,
        date: str,
        # event: str,
        # full_time_result: str,
        # count: int
):
    """
    Function's duties:
    1) Call the func get_events_for_sport_view() for result
    2) Get the moneyline from the returned dictionary
    3) Convert moneyline to the ratio
    4) Create a record with bet in DB
    5) Take into account the funds allocated for the bet in the table with the count
    """
    result = await place_a_bet_view(sport_id=sport_id, date=date)
    return result

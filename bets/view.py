import json
from datetime import datetime, timezone

import aiohttp
import pytz
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from bets.dao import bets_data
from bets.utils import check_events_in_redis
from redis_tools import redis_tools

base_url = "https://therundown-inc.api.blobr.app/free-trial/"
sports_headers = {
  "X-BLOBR-KEY": "Ur9jqPC1lD5aIai6p8RKmvqJDu9he9TX"
}


async def get_and_record_in_db_main_data_about_team_view(
        sport_id: int,
        session: AsyncSession,
):
    team_part = f"v2/sports/{sport_id}/teams"
    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(url=base_url + team_part, headers=sports_headers) as response:
            json_response: dict[str, list[dict]] = await response.json()
            json_response = json_response.get('teams')
    for team in json_response:  # type: dict
        await bets_data.create_club(
            name=team.get('name'),
            abbreviation=team.get('abbreviation'),
            record=team.get('record'),
            session=session,
        )
    return JSONResponse(
        content={'Message': 'All data successfully recorded in DB'}
    )


async def get_and_record_in_db_schedule_of_team_view(
        team_title: str,
        limit: int,
        sport_id: int,
        session: AsyncSession,
):
    schedule_part = f"v1/sports/{sport_id}/schedule"
    schedules_list = list()
    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(url=base_url+schedule_part, headers=sports_headers) as response:
            json_response: dict[str, list[dict]] = await response.json()
            count = 0
            for schedule in json_response.get('schedules'):  # type: dict
                for key, value in schedule.items():
                    if value == team_title and count != limit:
                        schedules_list.append(schedule)
                        count += 1
                        break
    for schedule in schedules_list:  # type: dict
        res_home_team_id = await bets_data.get_club_id(
            name=schedule.get('home_team'),
            session=session,
        )
        res_away_team_id = await bets_data.get_club_id(
            name=schedule.get('away_team'),
            session=session,
        )
        await bets_data.create_schedule_for_club(
            home_team=schedule.get('home_team'),
            away_team=schedule.get('away_team'),
            home_team_id=res_home_team_id,
            away_team_id=res_away_team_id,
            date_event=datetime.strptime(
                schedule.get('date_event'), '%Y-%m-%dT%H:%M:%SZ'
            ).replace(microsecond=0),
            home_score=schedule.update(home_score=0),
            away_score=schedule.update(away_score=0),
            league_name=schedule.get('league_name'),
            event_location=schedule.get('event_location'),
            session=session,
        )
    return JSONResponse(
        content={'Message': 'All data successfully recorded in DB'}
    )


async def get_events_for_sport_view(
        sport_id: int,
        date: str,
):
    event_part = f'/v1/sports/{sport_id}/events/{date}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url + event_part, headers=sports_headers) as response:
            json_response = await response.json()
            events = json_response.get('events')
            key = f'event: {sport_id}'
            await redis_tools.set_pair(key=key, value=json.dumps(jsonable_encoder(events)), expiry=300)
            return events


async def place_a_bet_view(sport_id: int, date: str):
    cached_result = await check_events_in_redis(sport_id=sport_id)
    if cached_result is None:
        cached_result = await get_events_for_sport_view(sport_id=sport_id, date=date)

    return cached_result


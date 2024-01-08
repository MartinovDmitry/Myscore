import json

import aiohttp
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from bets.dao import bets_data
from bets.utils import check_events_in_redis
from redis_tools import redis_tools

base_url = "https://therundown-inc.api.blobr.app/free-trial/"
sports_headers = {
  "X-BLOBR-KEY": "aKO5IueHAFFu5TZv8xJomNXu6GQsaZ1T"
}


async def get_main_data_about_team_view(
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


async def get_schedule_of_team_view(
        team_title: str,
        limit: int,
        sport_id: int,
):
    schedule_part = f"v1/sports/{sport_id}/schedule"
    schedules_list = list()
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url+schedule_part, headers=sports_headers) as response:
            json_response: dict[str, list[dict]] = await response.json()

            count = 0
            for schedule in json_response.get('schedules'):  # type: dict
                for key, value in schedule.items():
                    if value == team_title and count != limit:
                        schedules_list.append(schedule)
                        count += 1
                        break
            return schedules_list


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


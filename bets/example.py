import requests
from fastapi import APIRouter, Path, Query

router = APIRouter(
    prefix='/bets',
    tags=['Bets'],
)

base_url = "https://therundown-inc.api.blobr.app/free-trial/"
sports_headers = {
  "X-BLOBR-KEY": "aKO5IueHAFFu5TZv8xJomNXu6GQsaZ1T"
}


# Endpoint for getting all kinds of sports
@router.get('/sports')
async def get_sports():
    sports_part = "v1/sports"
    response = requests.get(url=base_url + sports_part, headers=sports_headers)
    return response.json()


@router.get('/sports/{sport_id}/team')
async def get_main_data_about_team(
        team_title: str = Query(default='Real Madrid'),
        sport_id: int = Path(),
):
    """
    Endpoint for getting team by title in chosen sport by id
    :param team_title: The title of required team
    :param sport_id: ID for spain Premier League (14)
    :return: Required team or None, if your title is invalid
    """
    team_part = f"v1/sports/{sport_id}/teams"
    response = requests.get(url=base_url + team_part, headers=sports_headers)
    json_response: dict[str, list[dict]] = response.json()
    # print(json_response)
    for team in json_response.get('teams'):  # type: dict
        # print(team)
        for key, value in team.items():
            if value == team_title:
                print(team)
                return team
    return None


@router.get('/sports/{sport_id}/schedule')
async def get_schedule_of_team(
        sport_id: int = Path(),
):
    schedule_part = f"v1/sports/{sport_id}/schedule"
    response = requests.get(url=base_url + schedule_part, headers=sports_headers)
    return response.json()


# Endpoint for getting event
@router.get('/event/{event_id}')
async def get_event_by_id(event_id: int):
    event_part = f"v2/events/{event_id}"
    response = requests.get(url=base_url + event_part, headers=sports_headers)
    return response.json()


# Endpoint for getting event
@router.get('/stats')
async def get_stats(sport_id: int):
    event_part = "v2/stats"
    response = requests.get(url=base_url + event_part, headers=sports_headers)
    return response.json()

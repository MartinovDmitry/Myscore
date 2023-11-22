import pytest
from httpx import AsyncClient
from sqlalchemy import JSON


@pytest.mark.parametrize('league_name, status_code', [
    ('LaLiga', 200),
    ('Bundesliga', 404),
])
async def test_get_league_by_title(
        league_name: str,
        status_code: int,
        async_client: AsyncClient,
):
    response = await async_client.get(
        f'/leagues/{league_name}'
    )
    assert response.status_code == status_code


@pytest.mark.parametrize('league_name, country, clubs_number, status_code', [
    ('LaLiga', 'Spain', 30, 409),  # case with already existed league
    ('Bundesliga', 'German', 28, 201),  # normal case
    ('Bundesliga', 'German', 28, 409),  # case with already existed league
    ('LaLiga', 'Spain', None, 422),  # case with validation error
])
async def test_create_league(
        league_name: str,
        country: str,
        clubs_number: int,
        status_code: int,
        async_client: AsyncClient,
):
    response = await async_client.post('/leagues/', json={
        'league_name': league_name,
        'country': country,
        'clubs_number': clubs_number,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('league_name, country, clubs_number, status_code', [
    ('LaLiga', 'Spain', 32, 200),  # normal case
    ('LaLigaa', 'Spain', 32, 404),  # case not found
    ('LaLiga', 'Spain', 'string', 422),  # case with validation error
])
async def test_update_league(
        league_name: str,
        country: str,
        clubs_number: int,
        status_code: int,
        async_client: AsyncClient,
):
    response = await async_client.put('/leagues/', json={
        'league_name': league_name,
        'country': country,
        'clubs_number': clubs_number,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('league_name, status_code', [
    ('LaLigaa', 404),
    ('LaLiga', 200),
])
async def test_delete_league(
        league_name: str,
        status_code: int,
        async_client: AsyncClient,
):
    response = await async_client.delete('/leagues/', params={
        'league_name': league_name,
    })
    assert response.status_code == status_code

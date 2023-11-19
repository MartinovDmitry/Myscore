from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from exceptions import WrongCredentialsException, AlreadyExistsException
from league.dao import LeagueDAO
from league.schemas import SchLeagueCreate, SchLeagueUpdated


async def get_league_by_title_view(
        league_name: str,
        session: AsyncSession,
):
    league = await LeagueDAO.get_league_by_title(
        league_name=league_name,
        session=session,
    )
    if league is None:
        raise WrongCredentialsException
    return league


async def create_league_view(
        league: SchLeagueCreate,
        session: AsyncSession,
):
    result = await LeagueDAO.get_league_by_title(
        league_name=league.league_name,
        session=session,
    )
    if result:
        raise AlreadyExistsException
    await LeagueDAO.create_league(
        league=league,
        session=session,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'Message': 'League is created'}
    )


async def update_league_view(
        league: SchLeagueUpdated,
        session: AsyncSession,
):
    result = await LeagueDAO.get_league_by_title(
        league_name=league.league_name,
        session=session,
    )
    if result is None:
        raise WrongCredentialsException
    await LeagueDAO.update_league(
        league=league,
        session=session,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'Message': 'League is updated'}
    )


async def delete_league_view(
        league_name: str,
        session: AsyncSession,
):
    result = await LeagueDAO.get_league_by_title(
        league_name=league_name,
        session=session,
    )
    if result is None:
        raise WrongCredentialsException
    await LeagueDAO.delete_league(
        league_name=league_name,
        session=session,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'Message': 'League is deleted'}
    )

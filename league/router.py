import asyncio
import time

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from league.dao import LeagueDAO
from league.schemas import SchLeagueCreate, SchLeagueResponse, SchLeagueUpdated, SchLeagueBase
from league.view import get_league_by_title_view, create_league_view, delete_league_view, update_league_view, \
    get_leagues_view
from permission import permission

router = APIRouter(
    prefix='/leagues',
    tags=['Leagues'],
)


@router.get('/{league_name}')
@cache(expire=30)
async def get_league_by_title(
        league_name: str,
        session: AsyncSession = Depends(session_factory),
) -> SchLeagueResponse:
    await asyncio.sleep(3)
    league = await get_league_by_title_view(
        league_name=league_name,
        session=session,
    )
    return league


@router.get('/')
async def get_leagues(
        session: AsyncSession = Depends(session_factory)
) -> list[SchLeagueResponse]:
    leagues = await get_leagues_view(
        session=session
    )
    return leagues


@router.post('/')
async def create_league(
        league: SchLeagueCreate,
        role: str = Depends(permission.check_role_admin_of_user),
        session: AsyncSession = Depends(session_factory),
) -> JSONResponse:
    response = await create_league_view(
        league=league,
        session=session,
    )
    return response


@router.put('/')
async def update_league(
        league: SchLeagueUpdated,
        role: str = Depends(permission.check_role_admin_of_user),
        session: AsyncSession = Depends(session_factory),
) -> JSONResponse:
    response = await update_league_view(
        league=league,
        session=session,
    )
    return response


@router.delete('/')
async def delete_league(
        league_name: str,
        role: str = Depends(permission.check_role_admin_of_user),
        session: AsyncSession = Depends(session_factory),
) -> JSONResponse:
    response = await delete_league_view(
        league_name=league_name,
        session=session,
    )
    return response

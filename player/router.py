from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from player.dao import PlayerDAO
from player.schemas import SchPlayerCreate, SchPlayerResponse
from player.view import get_player_by_name_view, create_player_view

router = APIRouter(
    prefix='/players',
    tags=['Players'],
)


@router.get('/')
async def get_player_by_name(
        first_name: str,
        second_name: str = None,
        session: AsyncSession = Depends(session_factory),
) -> list[SchPlayerResponse]:
    players = await get_player_by_name_view(
        first_name=first_name,
        second_name=second_name,
        session=session,
    )
    return players


@router.post('/')
async def create_player(
        player: SchPlayerCreate,
        session: AsyncSession = Depends(session_factory),
) -> JSONResponse:
    await create_player_view(
        player=player,
        session=session,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'Message': 'Player is created'},
    )

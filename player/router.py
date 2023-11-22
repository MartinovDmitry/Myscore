from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from player.dao import PlayerDAO
from player.schemas import SchPlayerCreate

# router = APIRouter(
#     prefix='/players',
#     tags=['players'],
# )
#
#
# @router.get('/')
# async def get_player_by_name(
#         first_name: str,
#         second_name: str = None,
#         session: AsyncSession = Depends(session_factory),
# ):
#     players = await PlayerDAO.get_player_by_name(
#         first_name=first_name,
#         second_name=second_name,
#         session=session,
#     )
#     return players
#
#
# @router.post('/')
# async def create_player(
#         player: SchPlayerCreate,
#         session: AsyncSession = Depends(session_factory),
# ) -> JSONResponse:
#     await PlayerDAO.create_player(
#         player=player,
#         session=session,
#     )
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content={'Message': 'Player is created'},
#     )

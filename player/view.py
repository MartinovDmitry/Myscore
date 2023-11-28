from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import WrongCredentialsException
from player.dao import PlayerDAO
from player.schemas import SchPlayerCreate


async def get_player_by_name_view(
        first_name: str,
        second_name: str,
        session: AsyncSession,
):
    players = await PlayerDAO.get_player_by_name(
        first_name=first_name,
        second_name=second_name,
        session=session,
    )
    if players is None:
        raise WrongCredentialsException
    return players


async def create_player_view(
        player: SchPlayerCreate,
        session: AsyncSession,
):
    players = await PlayerDAO.get_player_by_name(
        first_name=player.first_name,
        second_name=player.second_name,
        session=session,
    )
    if players is None:
        raise WrongCredentialsException
    await PlayerDAO.create_player(
        player=player,
        session=session,
    )

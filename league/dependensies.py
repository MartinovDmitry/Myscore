from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import AlreadyExistsException, WrongCredentialsException
from league.dao import LeagueDAO


async def league_is_not_none(
        league_name: str,
        session: AsyncSession,
):
    check_league = await LeagueDAO.get_league_by_title(
        league_name=league_name,
        session=session
    )
    if check_league:
        raise AlreadyExistsException
    return check_league


async def league_is_none(
        league_name: str,
        session: AsyncSession,
):
    check_league = await LeagueDAO.get_league_by_title(
        league_name=league_name,
        session=session
    )
    if check_league is None:
        raise WrongCredentialsException
    return check_league

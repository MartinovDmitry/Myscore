from sqlalchemy.ext.asyncio import AsyncSession

from bets_club.dao import DAOClub
from bets_club.schemas import SchStandingsResponse
from bets_club.utils import Schedule


async def get_standings_view(session: AsyncSession):
    standings = await DAOClub.get_standings(session=session)
    # standings_dto = [SchStandingsResponse.model_validate(row, from_attributes=True) for row in standings]
    # standings_dto = [Schedule.update_schedule(record) for record in standings_dto]
    standings_dto = [
        Schedule.update_schedule(SchStandingsResponse.model_validate(row, from_attributes=True)) for row in standings
    ]
    return standings_dto

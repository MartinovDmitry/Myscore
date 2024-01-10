from sqlalchemy import select, null
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from bets_club.models import PremierLeagueClub


class DAOClub:

    @staticmethod
    async def get_standings(session: AsyncSession):
        pl_club = aliased(PremierLeagueClub)
        query = (
            select(
                pl_club.name,
                null().label('total_matches'),
                pl_club.record,
                null().label('points')
            )
        )
        result = await session.execute(query)
        standings = result.all()
        return standings


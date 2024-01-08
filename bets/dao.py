from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bets_club.models import PremierLeagueClub


class BetsData:

    @staticmethod
    async def create_club(session: AsyncSession, **data):
        stmt = insert(PremierLeagueClub).values(**data)
        await session.execute(stmt)
        await session.commit()


bets_data = BetsData()

from datetime import datetime

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bets_club.models import PremierLeagueClub
from bets_schedule.models import PremierLeagueSchedule


class BetsData:

    @staticmethod
    async def get_club_id(session: AsyncSession, **data):
        query_team_id = select(PremierLeagueClub.id).filter_by(**data)
        res_team_id = await session.execute(query_team_id)
        return res_team_id.scalar_one_or_none()

    @staticmethod
    async def create_club(session: AsyncSession, **data):
        stmt = insert(PremierLeagueClub).values(**data)
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def create_schedule_for_club(
            away_team: str,
            home_team: str,
            session: AsyncSession,
            **data,
    ):
        stmt = insert(PremierLeagueSchedule).values(
            home_team=home_team,
            away_team=away_team,
            updated_at=datetime.utcnow(),
            **data
        )
        await session.execute(stmt)
        await session.commit()


bets_data = BetsData()

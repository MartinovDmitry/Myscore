from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from bets_schedule.models import PremierLeagueSchedule


class DAOSchedule:

    @staticmethod
    async def get_schedule_team_by_id(
            team_id: int,
            session: AsyncSession,
    ):
        pl_sch = aliased(PremierLeagueSchedule)
        sub_query = (
            select(
                pl_sch,
                func.concat(pl_sch.away_team, ' at ', pl_sch.home_team, ' - ', pl_sch.date_event).label('event_name'),
            )
            .where(or_(
                pl_sch.home_team_id == team_id,
                pl_sch.away_team_id == team_id))
            .subquery('helper_1')
        )
        cte = select(sub_query)
        result = await session.execute(cte)
        schedule = result.all()
        print(schedule)
        return schedule

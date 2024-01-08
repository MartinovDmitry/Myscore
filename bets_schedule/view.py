from sqlalchemy.ext.asyncio import AsyncSession

from bets_schedule.dao import DAOSchedule


async def get_schedule_team_by_id_view(
        team_id: int,
        session: AsyncSession,
):
    schedule = await DAOSchedule.get_schedule_team_by_id(
        team_id=team_id,
        session=session,
    )
    return schedule

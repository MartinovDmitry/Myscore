from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bets_schedule.schemas import SchScheduleResponse
from bets_schedule.view import get_schedule_team_by_id_view
from db_helper import session_factory

router = APIRouter(
    prefix='/schedule',
    tags=['Schedule'],
)


@router.get('/{team_id}')
async def get_schedule_team_by_id(
        team_id: int,
        session: AsyncSession = Depends(session_factory),
) -> list[SchScheduleResponse]:
    result = await get_schedule_team_by_id_view(
        team_id=team_id,
        session=session,
    )
    return result

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bets_club.schemas import SchStandingsResponse
from bets_club.view import get_standings_view
from db_helper import session_factory

router = APIRouter(
    prefix='/club',
    tags=['Club']
)


@router.get('/standings')
async def get_standings(
        session: AsyncSession = Depends(session_factory),
) -> list[SchStandingsResponse]:
    standings = await get_standings_view(session=session)
    return standings


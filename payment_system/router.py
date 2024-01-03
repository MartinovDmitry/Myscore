from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from payment_system.permission import check_permission_for_replenishment
from payment_system.view import replenishment_of_the_balance_view

router = APIRouter(
    prefix='/payment',
    tags=['Payment-system'],
)


@router.post('/')
async def replenishment_of_the_balance(
        user_id: int,
        count: int,
        session: AsyncSession = Depends(session_factory),
) -> JSONResponse:
    response = await replenishment_of_the_balance_view(
        user_id=user_id,
        count=count,
        session=session,
    )
    return response

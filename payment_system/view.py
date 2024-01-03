from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from payment_system.dao import PaymentDAO
from payment_system.permission import check_permission_for_replenishment


async def replenishment_of_the_balance_view(user_id: int, count: int, session: AsyncSession):
    await check_permission_for_replenishment(
        user_id=user_id, session=session
    )
    await PaymentDAO.balance_replenishment(
        user_id=user_id, count=count, session=session,
    )
    response = JSONResponse(
        content={'Message': f'Your balance is replenished on {count}'}
    )
    return response

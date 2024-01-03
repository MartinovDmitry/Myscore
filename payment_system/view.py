from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from payment_system.dao import PaymentDAO


async def replenishment_of_the_balance_view(user_id: int, count: int, session: AsyncSession):
    await PaymentDAO.balance_replenishment(
        user_id=user_id, count=count, session=session,
    )
    response = JSONResponse(
        content={'Message': f'Your balance is replenished on {count}'}
    )
    return response

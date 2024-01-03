from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from payment_system.models import Payment


class PaymentDAO:
    model = Payment

    @classmethod
    async def balance_replenishment(cls, user_id: int, count: int, session: AsyncSession):
        query = select(cls.model).where(cls.model.user_id == user_id)
        res = await session.execute(query)
        record_with_payment = res.scalar_one_or_none()
        if record_with_payment:
            stmt = (
                update(cls.model)
                .where(cls.model.user_id == user_id)
                .values(cls.model.count == cls.model.count + count)
            )
            await session.execute(stmt)
            await session.commit()
        else:
            stmt = (
                insert(cls.model)
                .values(
                    user_id=user_id,
                    count=count,
                    replenishment_at=datetime.utcnow()
                )
            )
            await session.execute(stmt)
            await session.commit()


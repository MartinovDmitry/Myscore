from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import PermissionVerifiedException
from users.models import User


async def check_permission_for_replenishment(
        user_id: int,
        session: AsyncSession
):
    query = select(User).where(and_(User.id == user_id, User.is_verified == True))
    res = await session.execute(query)
    verified_user = res.scalar_one_or_none()
    if verified_user is None:
        raise PermissionVerifiedException
    else:
        return True

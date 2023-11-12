from fastapi import Depends
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from users.models import User, RefreshToken


class UserDAO:
    model = User

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def create_user(cls, session: AsyncSession, **data):
        stmt = insert(cls.model).values(**data)
        await session.execute(stmt)
        await session.commit()


class TokenDAO:
    model = RefreshToken

    @classmethod
    async def create_token(cls, session: AsyncSession, **data):
        stmt = insert(cls.model).values(**data)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def update_refresh_token(cls, user_id: int, refresh_token: str, session: AsyncSession):
        stmt = (
            update(cls.model)
            .where(cls.model.user_id == user_id)
            .values(refresh_token=refresh_token)
        )
        payload = await session.execute(stmt)
        await session.commit()


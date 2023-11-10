from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from users.models import User


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

        
    
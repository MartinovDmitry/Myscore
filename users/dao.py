import json
from datetime import datetime, timedelta
from typing import NoReturn

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert, update, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db_helper import async_session
from exceptions import ALotOfRecordsRefreshTokens
from redis_tools import redis_tools
from users.models import User, RefreshToken


class UserDAO:
    model = User

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_with_context_manager(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def create_user(cls, session: AsyncSession, **data):
        stmt = insert(cls.model).values(**data)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def verify_user(cls, user_id: int, session: AsyncSession, **data):
        stmt = (
            update(cls.model)
            .where(cls.model.id == user_id)
            .values(**data)
        )
        await session.execute(stmt)
        await session.commit()


class TokenDAO:
    model = RefreshToken

    @classmethod
    async def create_token_record_in_db(cls, session: AsyncSession, **data):
        # Postgres
        stmt = insert(cls.model).values(**data)
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def create_token_record_in_redis(user_id: int, refresh_token: str):
        refresh_token_record = RefreshToken(
            refresh_token=refresh_token,
            user_id=user_id,
            expire_at=datetime.utcnow() + timedelta(minutes=settings.REFR_EXPIRE),
            created_at=datetime.utcnow(),
        )
        key = f'session:{user_id}'
        await redis_tools.set_pair(key=key, value=json.dumps(jsonable_encoder(refresh_token_record)), expiry=30)
        res = await redis_tools.get_pair(key)
        res = json.loads(res)
        print(res)

    @classmethod
    async def delete_token_records_in_db(cls, user_id: int, session: AsyncSession):
        stmt = delete(cls.model).where(cls.model.user_id == user_id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def check_count_of_max_record(cls, user_id: int, session: AsyncSession) -> NoReturn:
        query = select(func.count(cls.model.refresh_token)).where(cls.model.user_id == user_id)
        res = await session.execute(query)
        count = res.scalar_one_or_none()
        if count == 2:
            raise ALotOfRecordsRefreshTokens

    @classmethod
    async def update_refresh_token(cls, user_id: int, refresh_token: str, session: AsyncSession):
        stmt = (
            update(cls.model)
            .where(cls.model.user_id == user_id)
            .values(refresh_token=refresh_token)
        )
        await session.execute(stmt)
        await session.commit()


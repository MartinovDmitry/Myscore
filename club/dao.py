from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from club.models import Club
from club.schemas import SchClubCreate


class ClubDAO:
    model = Club

    @classmethod
    async def create_club(cls, club: SchClubCreate, session: AsyncSession):
        stmt = insert(cls.model).values(**club.model_dump())
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_club_by_title(cls, title: str, session: AsyncSession):
        query = select(cls.model).where(cls.model.title == title)
        result = await session.execute(query)
        return result

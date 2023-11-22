from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from league.models import League
from league.schemas import SchLeagueCreate, SchLeagueUpdated


class LeagueDAO:
    model = League

    @classmethod
    async def create_league(cls, league: SchLeagueCreate, session: AsyncSession):
        stmt = insert(cls.model).values(**league.model_dump())
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_leagues(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)
        leagues = result.scalars().all()
        return leagues

    @classmethod
    async def get_league_by_title(cls, league_name: str, session: AsyncSession):
        query = select(cls.model).where(cls.model.league_name == league_name)
        result = await session.execute(query)
        league = result.scalar_one_or_none()
        return league

    @classmethod
    async def update_league(cls, league: SchLeagueUpdated, session: AsyncSession):
        stmt = (
            update(cls.model)
            .where(cls.model.league_name == league.league_name)
            .values(**league.model_dump(exclude_unset=True))
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def delete_league(cls, league_name: str, session: AsyncSession):
        stmt = delete(cls.model).where(cls.model.league_name == league_name)
        await session.execute(stmt)
        await session.commit()

from typing import Generator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, sessionmaker

from config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'


if settings.MODE == "TEST":
    db_url = settings.test_db_url
    db_params = {'poolclass': NullPool}
else:
    db_url = settings.db_url
    db_params = {'pool_size': 5, 'max_overflow': 15}

engine = create_async_engine(
    db_url,
    echo=False,
    # pool_size=5,
    # max_overflow=15,
    **db_params,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def session_factory() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.close()

import asyncio
import json

import pytest_asyncio
from sqlalchemy import insert
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app as fastapi_app
from config import settings
from db_helper import Base, async_session, engine
from users.models import User, RefreshToken
from league.models import League


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'tests/mock_{model}.json', 'r') as file:
            return json.load(file)

    users = open_mock_json('users')
    leagues = open_mock_json('leagues')

    async with async_session() as session:
        add_users = insert(User).values(users)
        add_leagues = insert(League).values(leagues)

        await session.execute(add_users)
        await session.execute(add_leagues)
        await session.commit()


@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac

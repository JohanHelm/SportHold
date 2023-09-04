import asyncio
import pytest
import pytest_asyncio
from app.infra.db.pgdb.dal import Builder

URI_SYNC = "postgresql+psycopg2://postgres:qwerty123@127.0.0.1:5432/dev"
URI_ASYNC = "postgresql+asyncpg://postgres:qwerty123@127.0.0.1:5432/dev"


@pytest.fixture(scope="session")
def pg_session():
    repo = Builder(uri=URI_SYNC)
    session = repo.get_sync_session()
    return session


@pytest_asyncio.fixture(scope="function")
async def async_db_session():
    repo = Builder(uri=URI_ASYNC)
    session = repo.async_db_session()
    return session


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()



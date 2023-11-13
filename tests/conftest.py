import asyncio
import os
import pytest
import pytest_asyncio
from app.infra.db.pgdb.dal import Builder
from click.testing import CliRunner

URI_ASYNC = "postgresql+asyncpg://postgres:qwerty123@127.0.0.1:5432/dev"


@pytest_asyncio.fixture(scope="function")
async def async_db_session():
    repo = Builder(uri=URI_ASYNC)
    session = repo.async_db_session()
    return session


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def cli_runner():
    runner = CliRunner()
    return runner

@pytest.fixture(scope="function", autouse=True)
def set_env():
    os.environ["ENV"] = "DEV"
    os.environ["LOGLEVEL"] = "DEBUG"
    os.environ["LOGFILE"] = "./logs/logfile.log"
    os.environ["SETTING_FILE_PATH"] = "./conf/config.yaml"
    
import asyncio
from datetime import timedelta, time
import os
from click.testing import CliRunner
import pytest
import pytest_asyncio
from app.infra.db.pgdb.dal import Builder
from app.domain.models.object.dto import ObjectCreate
from app.infra.db.models.object.dao import ObjectDAO
from app.domain.models.schedule.dto import ScheduleCreate
from app.domain.models.user.dto import UserCreate, UserGet

URI_ASYNC = "postgresql+asyncpg://postgres:qwerty123@127.0.0.1:5432/dev"


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def session():
    repo = Builder(uri=URI_ASYNC, echo=False)
    return repo.get_session


@pytest.fixture(scope="function")
def test_object() -> ObjectCreate:
    return ObjectCreate(name="test", desc="test")


@pytest.fixture(scope="function")
def test_schedule() -> ScheduleCreate:
    test_schedule_pydantic = ScheduleCreate(
        name="Test schedule",
        desc="Description",
        days_open=[1, 2],
        open_from=time(9, 0, 0),
        open_until=time(18, 0, 0),
        min_book_time=timedelta(minutes=15),
        max_book_time=timedelta(minutes=30),
        time_step=timedelta(minutes=15),
    )
    return test_schedule_pydantic


@pytest.fixture(scope="function")
def test_user() -> UserCreate:
    test_user_pydantic = UserCreate(
        tg_id=123,
        first_name="anton",
        last_name="bezkrovny",
        username="@antonbezkrovnyy",
        language_code="ru",
        is_premium=True,
        is_bot=False,
    )
    return test_user_pydantic


@pytest.fixture(scope="function")
def test_user_get() -> UserCreate:
    test_user_pydantic = UserGet(
        id=1,
        tg_id=123,
        first_name="anton",
        last_name="bezkrovny",
        username="@antonbezkrovnyy",
        language_code="ru",
        is_premium=True,
        is_bot=False,
    )
    return test_user_pydantic


@pytest.fixture(scope="session")
def cli_runner():
    runner = CliRunner()
    return runner


@pytest.fixture(scope="function")
def set_env():
    os.environ["ENV"] = "DEVELOPMENT"
    os.environ["LOGLEVEL"] = "DEBUG"
    os.environ["LOGFILE"] = "./logs/logfile.log"
    os.environ["SETTING_FILE_PATH"] = "./conf/config.yaml"

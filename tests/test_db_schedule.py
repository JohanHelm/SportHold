from datetime import time, timedelta

import pytest
from app.domain.models.schedule.dto import ScheduleGet, ScheduleCreate
from app.infra.db.models.schedule.dao import ScheduleDAO

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_schedule_add(async_db_session):
    session = await async_db_session
    schedule_dao = ScheduleDAO(session)
    test_schedule_pydantic = ScheduleCreate(
        name="Test schedule",
        desc="Description",
        days_open=[1, 2],
        open_from=time(9, 0, 0),
        open_until=time(18, 0, 0),
        min_book_time=timedelta(minutes=15),
        max_book_time=timedelta(minutes=30),
        time_step=timedelta(minutes=15)
    )
    created_schedule: ScheduleGet = await schedule_dao.create(test_schedule_pydantic)
    pytest.test_schedule_id = created_schedule.id
    assert created_schedule.name == test_schedule_pydantic.name

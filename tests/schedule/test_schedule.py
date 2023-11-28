from datetime import datetime
import pytest
from app.domain.controllers.schedules import ScheduleManager

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_schedule_is_day_in_schedule(test_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    manager.add_schedule(test_schedule)
    assert manager.is_day_in_schedules(date=date) == True


@pytest.mark.asyncio
async def test_schedule_gen_slots(test_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    manager.add_schedule(test_schedule)
    slots = manager.generate_time_slots(test_schedule, date=date)
    assert slots is not None

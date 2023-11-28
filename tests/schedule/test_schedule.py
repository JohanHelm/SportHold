from datetime import datetime
import pytest
from app.domain.controllers.schedules import ScheduleManager

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_schedule_is_day_in_schedule(all_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    manager.add_schedule(all_days_schedule)
    assert manager.is_day_in_schedules(date=date) == True


@pytest.mark.asyncio
async def test_schedule_is_day_not_in_schedule(none_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    manager.add_schedule(none_days_schedule)
    assert manager.is_day_in_schedules(date=date) == False


@pytest.mark.asyncio
async def test_many_schedules(all_days_schedule, none_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    manager.add_schedule(none_days_schedule)
    manager.add_schedule(all_days_schedule)
    assert manager.is_day_in_schedules(date=date) == True


@pytest.mark.asyncio
async def test_schedule_gen_slots(all_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    manager.add_schedule(all_days_schedule)
    slots = manager.generate_time_slots(all_days_schedule, date=date)
    assert slots is not None

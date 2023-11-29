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
    current_schedules = manager.day_in_schedule(
        schedules=[none_days_schedule, all_days_schedule], date=date
    )
    assert all_days_schedule in current_schedules


@pytest.mark.asyncio
async def test_ident_schedules(all_days_schedule, none_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    current_schedules = manager.day_in_schedule(
        schedules=[all_days_schedule, all_days_schedule], date=date
    )
    assert all_days_schedule in current_schedules
    assert len(current_schedules) == 1


@pytest.mark.asyncio
async def test_schedule_gen_slots(all_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    slots = manager.generate_time_slots([all_days_schedule], date=date)
    assert slots is not None


@pytest.mark.asyncio
async def test_schedule_restricted_gen_slots(day_siesta_schedule, all_days_schedule):
    date = datetime.today()
    manager = ScheduleManager()
    slots = manager.generate_time_slots([all_days_schedule, day_siesta_schedule], date=date)
    current_date = date
    s = datetime(current_date.year, current_date.month, current_date.day, 16, 0)
    e = datetime(current_date.year, current_date.month, current_date.day, 17, 0)

    restricted_slot = [(s, e)]
    assert restricted_slot not in slots
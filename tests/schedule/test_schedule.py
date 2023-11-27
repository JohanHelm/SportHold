import datetime
import pytest
from app.domain.models.schedule.dto import ScheduleBase
from app.domain.models.schedule.controller import is_day_in_schedule
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.weekdays import DaysOfWeek
from app.domain.models.schedule.dto import ScheduleStatus
from app.helpers.maskers.weeks import WeeksInYear
from app.helpers.maskers.daysmonth import DaysInMonth

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_schedule_is_day_in_schedule():
    test_schedule = ScheduleBase()
    test_schedule.status = ScheduleStatus.ACTIVE
    test_schedule.mask_weeks = WeeksInYear.ALL
    test_schedule.mask_weekdays = DaysOfWeek.ALL
    test_schedule.mask_quartals = Quartals.ALL
    test_schedule.mask_days_month = DaysInMonth(sum(DaysInMonth))
    assert is_day_in_schedule(test_schedule, date=datetime.date(2023, 11, 27)) == True

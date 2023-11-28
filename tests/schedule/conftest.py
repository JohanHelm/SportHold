import pytest

from app.domain.models.schedule.dto import ScheduleBase, ScheduleStatus
from app.domain.models.slot.dto import SlotType
from app.helpers.maskers.daysmonth import DaysInMonth
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear

@pytest.fixture(scope="session")
def test_schedule():
    test_schedule = ScheduleBase()
    test_schedule.status = ScheduleStatus.ACTIVE
    test_schedule.mask_weeks = WeeksInYear.ALL
    test_schedule.mask_weekdays = DaysOfWeek.ALL
    test_schedule.mask_quartals = Quartals.ALL
    test_schedule.mask_days_month = DaysInMonth.ALL
    test_schedule.hour_start = 9
    test_schedule.hour_end = 18
    test_schedule.slot_max_time = 30
    test_schedule.slot_min_time = 15
    test_schedule.slot_step_time = 5
    test_schedule.slot_type = SlotType.ACCESSIBLE
    return test_schedule

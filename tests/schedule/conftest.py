import pytest

from app.domain.models.schedule.dto import ScheduleBase, ScheduleStatus
from app.domain.models.slot.dto import SlotType
from app.helpers.maskers.daysmonth import DaysInMonth
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear


@pytest.fixture(scope="session")
def all_days_schedule():
    test_schedule = ScheduleBase()
    test_schedule.name = "test all days"
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


@pytest.fixture(scope="session")
def none_days_schedule():
    none_days_schedule = ScheduleBase()
    none_days_schedule.name = "test none days"
    none_days_schedule.status = ScheduleStatus.ACTIVE
    none_days_schedule.mask_weeks = WeeksInYear.ALL
    none_days_schedule.mask_weekdays = DaysOfWeek.ALL
    none_days_schedule.mask_quartals = Quartals.NONE
    none_days_schedule.mask_days_month = DaysInMonth.ALL
    none_days_schedule.hour_start = 9
    none_days_schedule.hour_end = 18
    none_days_schedule.slot_max_time = 30
    none_days_schedule.slot_min_time = 15
    none_days_schedule.slot_step_time = 5
    none_days_schedule.slot_type = SlotType.ACCESSIBLE
    return none_days_schedule

@pytest.fixture(scope="session")
def day_siesta_schedule():
    none_days_schedule = ScheduleBase()
    none_days_schedule.name = "siesta 16-17 test none days"
    none_days_schedule.status = ScheduleStatus.ACTIVE
    none_days_schedule.mask_weeks = WeeksInYear.ALL
    none_days_schedule.mask_weekdays = DaysOfWeek.ALL
    none_days_schedule.mask_quartals = Quartals.NONE
    none_days_schedule.mask_days_month = DaysInMonth.ALL
    none_days_schedule.hour_start = 16
    none_days_schedule.hour_end = 17
    none_days_schedule.slot_max_time = 30
    none_days_schedule.slot_min_time = 15
    none_days_schedule.slot_step_time = 5
    none_days_schedule.slot_type = SlotType.RESTRICTED
    return none_days_schedule


from datetime import datetime, timedelta

from app.domain.models.schedule.dto import ScheduleStatus
from app.helpers.maskers.daysmonth import DaysInMonth
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear


class ScheduleManager:
    def __init__(self) -> None:
        self.schedules = []

    def add_schedule(self, schedule):
        self.schedules.append(schedule)

    def clear(self):
        self.schedules = []

    def find_nth_weekday_in_month(year, month, weekday, n):
        d = datetime(year, month, 1)
        while d.weekday() != weekday:
            d += datetime.timedelta(days=1)

        d += datetime.timedelta(weeks=n - 1)

        return d

    def check_schedule_date(self, schedule, date):
        if schedule.status == ScheduleStatus.NOT_ACTIVE:
            return False
        if schedule.valid_from > date.date():
            return False
        if (schedule.valid_from + schedule.valid_for_days) < date.date():
            return False
        if DaysOfWeek(2 ** date.date().isoweekday()) not in schedule.mask_weekdays:
            print(DaysOfWeek(2 ** date.date().isoweekday()))
            return False
        if WeeksInYear(2 ** date.date().isocalendar().week) not in schedule.mask_weeks:
            print(WeeksInYear(2 ** date.date().isocalendar().week))
            return False
        if (
            Quartals(2 ** ((date.date().month - 1) // 3 + 1))
            not in schedule.mask_quartals
        ):
            print(Quartals(2 ** ((date.date().month - 1) // 3 + 1)))
            return False
        if DaysInMonth(2 ** (date.date().day)) not in schedule.mask_days_month:
            print(DaysInMonth(2 ** (date.date().day)))
            return False
        if schedule.nth_weekday and schedule.nth_index:
            if date.date() != self.find_nth_weekday_in_month(
                date.date().year,
                date.date().month,
                schedule.nth_weekday,
                schedule.nth_index,
            ):
                return False
        return True

    def is_day_in_schedules(self, date: datetime) -> bool:
        return all(
            [self.check_schedule_date(schedule, date) for schedule in self.schedules]
        )
    def generate_time_slots(self, schedule, date):
        step = schedule.slot_step_time
        smax = schedule.slot_max_time
        smin = schedule.slot_min_time
        start = schedule.hour_start
        end = schedule.hour_end
        policy = schedule.policy_merge

        current_date = date

        s = datetime(current_date.year, current_date.month, current_date.day, start, 0)
        e = datetime(current_date.year, current_date.month, current_date.day, end, 0)
        time_slots = []
        while s + timedelta(minutes=smax) <= e:
            duration = smax
            if s + timedelta(minutes=duration) <= e:
                time_slots.append(
                    (
                        s,
                        s + timedelta(minutes=duration),
                    )
                )
            s += timedelta(minutes=smax)
        return time_slots
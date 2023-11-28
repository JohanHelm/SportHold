import datetime
from typing import List
from xmlrpc.client import Boolean
from .dto import ScheduleBase, ScheduleStatus
from app.domain.models.record.dto import RecordBase
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.daysmonth import DaysInMonth


class ScheduleController:
    ...


def find_nth_weekday_in_month(year, month, weekday, n):
    # Находим первый день недели в месяце
    d = datetime(year, month, 1)
    while d.weekday() != weekday:
        d += datetime.timedelta(days=1)

    # Переходим к нужной неделе
    d += datetime.timedelta(weeks=n - 1)

    # Возвращаем дату
    return d


def is_day_in_schedule(schedule: ScheduleBase, date: datetime) -> Boolean:
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
    if Quartals(2 ** ((date.date().month - 1) // 3 + 1)) not in schedule.mask_quartals:
        print(Quartals(2 ** ((date.date().month - 1) // 3 + 1)))
        return False
    if DaysInMonth(2 ** (date.date().day)) not in schedule.mask_days_month:
        print(DaysInMonth(2 ** (date.date().day)))
        return False
    if schedule.nth_weekday and schedule.nth_index:
        if date.date() != find_nth_weekday_in_month(
            date.date().year,
            date.date().month,
            schedule.nth_weekday,
            schedule.nth_index,
        ):
            return False
    return True


def generate_time_slots(schedule: ScheduleBase, date):
    step = schedule.slot_step_time
    smax = schedule.slot_max_time
    smin = schedule.slot_min_time
    start = schedule.hour_start
    end = schedule.hour_end
    policy = schedule.policy_merge

    date = datetime.date(year=2023, month=11, day=27)

    s = datetime.datetime(
        year=date.year, month=date.month, day=date.day, hour=start, minute=0
    )
    # e = datetime.datetime(date.year, date.month, date.day, hour=end)
    # time_slots = []
    # while s + datetime.timedelta(minutes=smax) <= end:
    #     duration = smax
    #     if current_time + datetime.timedelta(minutes=duration) <= end:
    #         time_slots.append(
    #             (
    #                 current_time,
    #                 current_time + datetime.timedelta(minutes=duration),
    #             )
    #         )
    #     current_time += datetime.timedelta(minutes=smax)
    # return time_slots

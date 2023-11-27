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


def is_day_in_schedule(schedule: ScheduleBase, date: datetime.date) -> Boolean:
    records = []
    today = date
    if schedule.status == ScheduleStatus.NOT_ACTIVE:
        return False
    if schedule.valid_from > today:
        return False
    if schedule.valid_from + schedule.valid_for_days < today:
        return False
    if DaysOfWeek(2 ** today.isoweekday()) not in schedule.mask_weekdays:
        return False
    if WeeksInYear(2 ** today.isocalendar().week) not in schedule.mask_weeks:
        return False
    # if Quartals(2**((today.month-1)//3 + 1)) not in schedule.mask_quartals:
    #     return False
    if DaysInMonth(2 ** (today.day)) not in schedule.mask_days_month:
        return False
    if schedule.nth_weekday and schedule.nth_weekday:
        if today != find_nth_weekday_in_month(
            today.year, today.month, schedule.nth_weekday, schedule.nth_index
        ):
            return False
    return True

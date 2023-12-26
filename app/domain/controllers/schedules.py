from typing import Set
from datetime import datetime, timedelta

from app.domain.models.schedule.dto import ScheduleBase, ScheduleStatus
from app.domain.models.slot.dto import SlotType
from app.helpers.maskers.daysmonth import DaysInMonth
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear


class TemporarySlot:
    def __init__(self, start: datetime, end: datetime, schedule_id):
        self.start = start
        self.end = end
        self.schedule_id = schedule_id

    def __str__(self):
        return f"{self.start}\n" \
               f"{self.end}"


class ScheduleManager:
    """
    Обрабатывает связку - лист расписаний и день - Выдает кортеж подходящих расписаний на день
    Обрабатывает кортеж расписаний на день - выдает список слотов на день
    """

    def find_nth_weekday_in_month(self, year, month, weekday, n):
        d = datetime(year, month, 1)
        while d.weekday() != weekday:
            d += timedelta(days=1)

        d += timedelta(weeks=n - 1)

        return d

    def is_date_in_schedule(self, schedule, date):
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

    def is_day_in_schedules(self, schedules, date: datetime) -> Set[ScheduleBase]:
        res = set(
            schedule
            for schedule in schedules
            if self.is_date_in_schedule(schedule, date)
        )
        return res

    def get_time_intervals_from_schedule(self, schedule, date):
        smax = schedule.slot_max_time
        start = schedule.hour_start
        end = schedule.hour_end
        current_date = date
        time_slots = []
        s = datetime(current_date.year, current_date.month, current_date.day, start, 0)
        e = datetime(current_date.year, current_date.month, current_date.day, end, 0)
        while s + timedelta(minutes=smax) <= e:
            duration = smax
            if s + timedelta(minutes=duration) <= e:
                temporary_slot = TemporarySlot(s, s + timedelta(minutes=duration), schedule.schedule_id)
                time_slots.append(temporary_slot)
            s += timedelta(minutes=smax)
        return time_slots

    def remove_overlapping_time_intervals(self, allowed_slots, forbidden_slots):
        cleaned_slots = []
        for slot in allowed_slots:
            overlap = False
            for forbidden_slot in forbidden_slots:
                if slot.start < forbidden_slot.end and slot.end > forbidden_slot.start:
                    overlap = True
                    break
            if not overlap:
                cleaned_slots.append(slot)
        return cleaned_slots

    def generate_time_intervals(self, schedules, date):
        access_schedule = [
            schedule
            for schedule in schedules
            if SlotType(schedule.slot_type) == SlotType.ACCESSIBLE
        ]
        restrict_schedule = [
            schedule
            for schedule in schedules
            if SlotType(schedule.slot_type) == SlotType.RESTRICTED
        ]
        # cleaned_slots = []
        allowed_slots = []
        forbidden_slots = []
        for schedule in access_schedule:
            schedule_slots = self.get_time_intervals_from_schedule(schedule, date)
            allowed_slots.extend(schedule_slots)

        for schedule in restrict_schedule:
            schedule_slots = self.get_time_intervals_from_schedule(schedule, date)
            forbidden_slots.extend(schedule_slots)

        cleaned_slots = self.remove_overlapping_time_intervals(
            allowed_slots, forbidden_slots
        )
        return cleaned_slots

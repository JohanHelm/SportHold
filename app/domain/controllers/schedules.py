from typing import List, Set
from datetime import datetime, timedelta

from app.domain.models.schedule.dto import ScheduleBase, ScheduleStatus
from app.domain.models.slot.dto import SlotType
from app.helpers.maskers.daysmonth import DaysInMonth
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear


class ScheduleManager:
    """
    Обрабатывает связку - лист расписаний и день - Выдает кортеж подходящих расписаний на день
    Обрабатывает кортеж расписаний на день - выдает список слотов на день
    """

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

    def day_in_schedule(self, schedules, date: datetime) -> Set[ScheduleBase]:
        res = set(
            schedule
            for schedule in schedules
            if self.check_schedule_date(schedule, date)
        )
        return res

    def slots_from_schedule(self, schedule, date):
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
                time_slots.append(
                    (
                        s,
                        s + timedelta(minutes=duration),
                    )
                )
            s += timedelta(minutes=smax)
        return time_slots
    def remove_overlapping_slots(self,allowed_slots, forbidden_slots):
        cleaned_slots = []
        for slot in allowed_slots:
            overlap = False
            for forbidden_slot in forbidden_slots:
                if slot[0] < forbidden_slot[1] and slot[1] > forbidden_slot[0]:
                    overlap = True
                    break
            if not overlap:
                cleaned_slots.append(slot)
        return cleaned_slots
    
    def generate_time_slots(self, schedules, date):
        access_schedule = [
            schedule
            for schedule in schedules
            if schedule.slot_type == SlotType.ACCESSIBLE
        ]
        restrict_schedule = [
            schedule
            for schedule in schedules
            if schedule.slot_type == SlotType.RESTRICTED
        ]
        cleaned_slots = []
        allowed_slots = []
        forbidden_slots = []
        for schedule in access_schedule:
            schedule_slots = self.slots_from_schedule(schedule, date)
            allowed_slots.extend(schedule_slots)

        for schedule in restrict_schedule:
            schedule_slots = self.slots_from_schedule(schedule, date)
            forbidden_slots.extend(schedule_slots)

        cleaned_slots = self.remove_overlapping_slots(allowed_slots, forbidden_slots)
        return cleaned_slots
            

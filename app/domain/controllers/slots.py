from typing import Set
from datetime import date, datetime, timedelta

from app.domain.models.schedule.dto import ScheduleModel
from app.domain.helpers.enums import DaysOfWeek, ScheduleStatus, SlotStatus, SlotType
from app.domain.models.slot.dto import SlotModel, SlotData


class SlotManager:
    """
    Обрабатывает связку - лист расписаний и день - Выдает кортеж подходящих расписаний на день
    Обрабатывает кортеж расписаний на день - выдает список слотов на день
    """

    def is_date_in_schedule(self, schedule: ScheduleModel, date: date):
        if schedule.status == ScheduleStatus.INACTIVE:
            return False
        if schedule.started > date.date():
            return False
        if schedule.ended < date.date():
            return False
        if DaysOfWeek(2 ** date.date().isoweekday()) not in schedule.mask_weekdays:
            return False
        return True

    def suitable_schedules(self, schedules, date: datetime) -> Set[ScheduleModel]:
        suitable_schedules = set(
            schedule
            for schedule in schedules
            if self.is_date_in_schedule(schedule, date)
        )
        return suitable_schedules

    def get_time_slots_from_schedule(self, schedule, date):
        slot_time = schedule.slot_time
        start = schedule.hour_start
        end = schedule.hour_end
        current_date = date
        time_slots = []
        s = datetime(current_date.year, current_date.month, current_date.day, start, 0)
        e = datetime(current_date.year, current_date.month, current_date.day, end, 0)
        while s + timedelta(minutes=slot_time) <= e:
            if s + timedelta(minutes=slot_time) <= e:
                temporary_slot = SlotModel(
                    started=s, ended=s + timedelta(minutes=slot_time)
                )
                time_slots.append(temporary_slot)
            s += timedelta(minutes=slot_time)
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

    def generate_time_intervals(self, schedules, date) -> SlotData:
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
        slots_data = SlotData(slots=cleaned_slots)
        return slots_data

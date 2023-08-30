import datetime

from src.models.schedules import BaseSchedule
from datetime import timedelta

class SchedulesController:
    def __init__(self, db):
        self.db = db

    def save_schedule(self, schedule: BaseSchedule):
        schedule = self.db.save_schedule(schedule)
        return schedule

    def get_schedule(self, uuid):
        schedule: BaseSchedule = self.db.get_schedule(uuid)
        return schedule

    def generate_slots(self,
                       uuid,
                       interval: timedelta = timedelta(hours=3),
                       dt_from: datetime = datetime.datetime.now()):
        schedule: BaseSchedule = self.db.get_schedule(uuid)

        min_step = schedule.time_step

        first_slot = datetime.datetime(
            year=dt_from.year,
            month=dt_from.month,
            day=dt_from.day,
            hour=dt_from.hour,
            minute=0
        )

        while first_slot < dt_from:
            first_slot = first_slot + min_step

        slots = [first_slot]
        current_slot = first_slot + min_step

        while current_slot < dt_from + interval:
            slots.append(current_slot)
            current_slot = current_slot + min_step

        return slots


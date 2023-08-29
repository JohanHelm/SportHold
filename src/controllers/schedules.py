import datetime
import math
import time

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

    def generate_slots(self, uuid, interval: timedelta = timedelta(hours=2)):
        schedule: BaseSchedule = self.db.get_schedule(uuid)
        time_delta_in_minutes = schedule.slot_time_delta.total_seconds() / 60
        hour_interval_count = int(60 / time_delta_in_minutes)
        slots_count = int(hour_interval_count * interval.total_seconds() / 60 / 60)
        now = datetime.datetime.now()
        d1 = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=0)
        slots = []
        for i in range(slots_count):
            min = i * time_delta_in_minutes
            slots.append(d1 + timedelta(minutes=min))

        return slots


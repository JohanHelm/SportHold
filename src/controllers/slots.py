from datetime import datetime, timedelta

from src.models.slots import BaseSlot
from src.models.users import BaseUser


class SlotsController:
    def __init__(self, db):
        self.db = db

    def save_slot(self, slot: BaseSlot):
        slot = self.db.save_slot(slot)
        return slot

    def get_slot(self, uuid):
        slot: BaseSlot = self.db.get_slot(uuid)
        return slot

    def create_slot(self, schedule_id, datetime_started: datetime, dt: timedelta):
        current_slot = BaseSlot(
            schedule_id=schedule_id,
            start_date=datetime_started.date(),
            start_time=datetime_started.time(),
            timedelta=dt,
            queue=[]
        )
        return current_slot

    def slot_add_member_to_queue(self, current_slot: BaseSlot, member: BaseUser):
        current_slot.queue.append(member)
        return current_slot



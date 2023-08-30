import datetime
from datetime import timedelta

from src.models.slots import BaseSlot
from src.controllers.slots import SlotsController
from src.controllers.memorydb import InMemoryDB
from uuid import UUID, uuid4

db = InMemoryDB
slot_control = SlotsController(db)

def test_regular_slot_creation():
    result_slot: BaseSlot = slot_control.create_slot(
        uuid4(),
        datetime.datetime(
            year=2023, month=10, day=1,
            hour=6, minute=30
        ),
        dt=timedelta(minutes=15)
    )
    assert result_slot.queue == []

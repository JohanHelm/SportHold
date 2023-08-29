from src.models.slots import BaseSlot
from datetime import date, time, timedelta


def test_regular_slot_creation():
    testSlot = BaseSlot(
        start_date=date(2023, 10, 3),
        start_time=time(16, 25, 0),
        timedelta=timedelta(minutes=30),
        queue = []
    )

    assert testSlot.start_date == date(2023, 10, 3)

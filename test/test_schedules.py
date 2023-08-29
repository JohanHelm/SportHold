import uuid

from src.models.schedules import BaseSchedule
from datetime import time, timedelta
from src.controllers.schedules import SchedulesController
from src.controllers.memorydb import InMemoryDB

db = InMemoryDB
schedule_control = SchedulesController(db)


def test_regular_schedule_create_and_retvive():
    test_schedule = BaseSchedule(
        name="Test Schedule",
        days_open=["mon", "fri"],
        open_from=time(9, 0, 0),
        open_until=time(18, 0, 0),
        min_book_time=timedelta(minutes=15),
        max_book_time=timedelta(minutes=30),
        slot_time_delta=timedelta(minutes=15),
    )

    test_schedule = schedule_control.save_schedule(test_schedule)
    assert test_schedule == schedule_control.get_schedule(test_schedule.id)


def test_generate_slots():
    test_schedule = BaseSchedule(
        name="Test Schedule",
        days_open=["mon", "fri"],
        open_from=time(9, 0, 0),
        open_until=time(18, 0, 0),
        min_book_time=timedelta(minutes=15),
        max_book_time=timedelta(minutes=30),
        slot_time_delta=timedelta(minutes=15),
    )
    test_schedule = schedule_control.save_schedule(test_schedule)
    slots = schedule_control.generate_slots(test_schedule.id)
    print("s " + str(slots))


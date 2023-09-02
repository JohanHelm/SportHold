import datetime

from app.domain.models import BaseSchedule
from datetime import time, timedelta
from app.infra.db import SchedulesController
from app.infra.db import InMemoryDB

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
        time_step=timedelta(minutes=15),
    )
    test_schedule = schedule_control.save_schedule(test_schedule)
    generated_slots = schedule_control.generate_slots(
        test_schedule.id,
        interval=timedelta(hours=2),
        dt_from=datetime.datetime(
            year=2023,
            month=10,
            day=1,
            hour=9,
            minute=21
        )
    )
    expected_result = [
        datetime.datetime(2023, 10, 1, 9, 30),
        datetime.datetime(2023, 10, 1, 9, 45),
        datetime.datetime(2023, 10, 1, 10, 0),
        datetime.datetime(2023, 10, 1, 10, 15),
        datetime.datetime(2023, 10, 1, 10, 30),
        datetime.datetime(2023, 10, 1, 10, 45),
        datetime.datetime(2023, 10, 1, 11, 0),
        datetime.datetime(2023, 10, 1, 11, 15)
    ]

    assert generated_slots == expected_result


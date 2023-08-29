from src.models.schedules import BaseSchedule
from datetime import date, time, timedelta


def test_regular_slot_creation():
    testSchedule = BaseSchedule(
        days_open=["mon", "fri"],
        open_from=time(9, 0, 0),
        open_until=time(18, 0, 0),
        min_book_time=timedelta(minutes=20),
        max_book_time=timedelta(minutes=40),
        time_grid=[],
        slots=[]
    )

    assert testSchedule.days_open == ["mon", "fri"]

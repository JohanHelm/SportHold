from datetime import datetime
from app.helpers.maskers.weekdays import DaysOfWeek

def test_all_days():
    today = datetime.today()
    weekday_bit = 2 ** today.weekday()
    weekday_mask = DaysOfWeek.ALL
    assert DaysOfWeek(weekday_bit) in weekday_mask


def test_monday_days():
    today = datetime(2023,11,27)
    weekday_bit = 2 ** today.weekday()
    weekday_mask = DaysOfWeek.Monday
    assert DaysOfWeek(weekday_bit) in weekday_mask

def test_sunday_days():
    today = datetime(2023,11,26)
    weekday_bit = 2 ** today.weekday()
    weekday_mask = DaysOfWeek.Sunday
    assert DaysOfWeek(weekday_bit) in weekday_mask
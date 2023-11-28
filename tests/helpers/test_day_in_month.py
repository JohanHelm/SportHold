from datetime import datetime
from app.helpers.maskers.daysmonth import DaysInMonth

def test_all_days():
    today = datetime.today()
    day_in_month_bit = 2 ** today.day
    day_in_month_mask = DaysInMonth.ALL
    assert DaysInMonth(day_in_month_bit) in day_in_month_mask


def test_1th_days():
    today = datetime(2023,1,1)
    day_in_month_bit = 2 ** today.day
    day_in_month_mask = DaysInMonth.DAY1
    assert DaysInMonth(day_in_month_bit) in day_in_month_mask

def test_31th_days():
    today = datetime(2023,12,31)
    day_in_month_bit = 2 ** today.day
    day_in_month_mask = DaysInMonth.DAY31
    assert DaysInMonth(day_in_month_bit) in day_in_month_mask
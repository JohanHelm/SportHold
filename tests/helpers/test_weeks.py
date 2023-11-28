from datetime import datetime
from app.helpers.maskers.weeks import WeeksInYear

def test_all_weeks():
    today = datetime.today()
    weekbit = 2 ** today.isocalendar().week
    week_mask = WeeksInYear.ALL
    assert WeeksInYear(weekbit) in week_mask

def test_first_weeks():
    today = datetime(2023, 1, 2)
    weekbit = 2 ** (today.isocalendar().week)
    week_mask = WeeksInYear.WEEK1
    assert WeeksInYear(weekbit) in week_mask

def test_last_week():
    today = datetime(2022, 12, 31)
    weekbit = 2 ** (today.isocalendar().week)
    week_mask = WeeksInYear.WEEK52
    assert WeeksInYear(weekbit) in week_mask

def test_48_week():
    today = datetime(2023, 11, 28)
    weekbit = 2 ** (today.isocalendar().week)
    week_mask = WeeksInYear.WEEK48
    assert WeeksInYear(weekbit) in week_mask
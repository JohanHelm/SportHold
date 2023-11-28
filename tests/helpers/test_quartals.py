from datetime import datetime
from app.helpers.maskers.quartals import Quartals


def test_all_quartals():
    today = datetime.today()
    quartal = (today.month - 1) // 3 + 1
    quartal_bit = 2**quartal
    quartal_mask = Quartals.ALL
    assert Quartals(quartal_bit) in quartal_mask


def test_1th_quartals():
    today = datetime(2023, 1, 1)
    quartal = (today.month - 1) // 3 + 1
    quartal_bit = 2**quartal
    quartal_mask = Quartals.First
    assert Quartals(quartal_bit) in quartal_mask


def test_2th_quartals():
    today = datetime(2023, 4, 1)
    quartal = (today.month - 1) // 3 + 1
    quartal_bit = 2**quartal
    quartal_mask = Quartals.Second
    assert Quartals(quartal_bit) in quartal_mask


def test_3th_quartals():
    today = datetime(2023, 7, 1)
    quartal = (today.month - 1) // 3 + 1
    quartal_bit = 2**quartal
    quartal_mask = Quartals.Thrid
    assert Quartals(quartal_bit) in quartal_mask

def test_4th_quartals():
    today = datetime(2023, 10, 1)
    quartal = (today.month - 1) // 3 + 1
    quartal_bit = 2**quartal
    quartal_mask = Quartals.Fourth
    assert Quartals(quartal_bit) in quartal_mask

def test_last_month_quartals():
    today = datetime(2023, 12, 1)
    quartal = (today.month - 1) // 3 + 1
    quartal_bit = 2**quartal
    quartal_mask = Quartals.Fourth
    assert Quartals(quartal_bit) in quartal_mask
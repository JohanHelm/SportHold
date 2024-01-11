from sys import prefix
from aiogram.filters.callback_data import CallbackData


class RentalsCallbackFactory(CallbackData, prefix="rentals"):
    step: int


class SlotsCallbackFactory(CallbackData, prefix="slots"):
    step: int


class OrdinalDayFactory(CallbackData, prefix="calendar"):
    day: int


rental_forward_callback_data = RentalsCallbackFactory(step=1).pack()
rental_back_callback_data = RentalsCallbackFactory(step=-1).pack()

slot_forward_callback_data = RentalsCallbackFactory(step=1).pack()
slot_back_callback_data = RentalsCallbackFactory(step=-1).pack()


def booking_date_callback_data(day: int):
    return OrdinalDayFactory(day=day).pack()

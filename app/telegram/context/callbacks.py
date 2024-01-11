from aiogram.filters.callback_data import CallbackData


class RentalsCallbackFactory(CallbackData, prefix="rentals"):
    step: int


rental_forward_callback_data = RentalsCallbackFactory(step=1).pack()
rental_back_callback_data = RentalsCallbackFactory(step=-1).pack()
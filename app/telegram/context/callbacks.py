from aiogram.filters.callback_data import CallbackData


class RentalsCallbackFactory(CallbackData, prefix="rentals"):
    step: int


forward_callback_data = RentalsCallbackFactory(step=1).pack()
back_callback_data = RentalsCallbackFactory(step=-1).pack()
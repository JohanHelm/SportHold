from aiogram.types import InlineKeyboardButton

from app.telegram.context.querys import Book, Nav, Records, RentalQuerys
from app.telegram.context.callbacks import (
    booking_date_callback_data,
    rental_back_callback_data,
    rental_forward_callback_data,
)

BTN_GO_TO_MAIN = InlineKeyboardButton(text="В меню", callback_data=Nav.TO_MAIN)
BTN_BACK_TO_RENTALS = InlineKeyboardButton(
    text="К списку объектов", callback_data=RentalQuerys.BACK
)

SHOW_RENTALS_BTN = InlineKeyboardButton(
    text="Доступные объекты!", callback_data=RentalQuerys.SHOW_RENTALS
)
USER_RECORDS_BTN = InlineKeyboardButton(
    text="Мои записи", callback_data=Records.SHOW_USER_RECORDS
)

RENTAL_BACKWARD_BTN = InlineKeyboardButton(
    text="<<", callback_data=rental_back_callback_data
)
RENTAL_FORWARD_BTN = InlineKeyboardButton(
    text=">>", callback_data=rental_forward_callback_data
)
SELECT_BOOKING_DATE_BTN = InlineKeyboardButton(
    text="К выбору даты записи.",
    callback_data=Book.SELECT_BOOK_DAY,
)


def calendar_button(button_text, day):
    data = booking_date_callback_data(day)
    return InlineKeyboardButton(text=button_text, callback_data=data)

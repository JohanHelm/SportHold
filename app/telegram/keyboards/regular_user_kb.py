from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_first_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    show_rentals_btn = InlineKeyboardButton(text='Объекты!', callback_data='show_rentals/0')
    kb_builder.row(show_rentals_btn)
    return kb_builder.as_markup()


def create_pagination_keyboard(rental_number, total_rentals) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    backward_btn = InlineKeyboardButton(text='<<', callback_data='shift_show_rentals/-1')
    forward_btn = InlineKeyboardButton(text='>>', callback_data='some special callback data')
    rental_button = InlineKeyboardButton(text=f"{rental_number}/{total_rentals} Расписание",
                                         callback_data=f"schedule {rental_number}/{total_rentals}")
    if rental_number == 1:
        kb_builder.row(rental_button, forward_btn)
    elif rental_number == total_rentals:
        kb_builder.row(backward_btn, rental_button)
    else:
        kb_builder.row(backward_btn, rental_button, forward_btn)
    return kb_builder.as_markup()

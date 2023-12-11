from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def create_pagination_keyboard(rental_number, total_rentals) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    backward_btn = InlineKeyboardButton(text='<<', callback_data='backward')
    forward_btn = InlineKeyboardButton(text='>>', callback_data='forward')
    rental_button = InlineKeyboardButton(text=f"{rental_number}/{total_rentals} Расписание", callback_data=f"{rental_number}/{total_rentals} schedule")
    if rental_number == 1:
        kb_builder.row(rental_button, forward_btn)
    elif rental_number == total_rentals:
        kb_builder.row(backward_btn, rental_button)
    else:
        kb_builder.row(backward_btn, rental_button, forward_btn)
    return kb_builder.as_markup()

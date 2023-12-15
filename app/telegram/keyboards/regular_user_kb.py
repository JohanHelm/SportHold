from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_first_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    show_rentals_btn = InlineKeyboardButton(text='Объекты!', callback_data='show_rentals')
    kb_builder.row(show_rentals_btn)
    return kb_builder.as_markup()


def create_rental_pagination_keyboard(rental_number, total_rentals) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    backward_btn = InlineKeyboardButton(text='<<', callback_data='shift_show_rentals/-1')
    forward_btn = InlineKeyboardButton(text='>>', callback_data='shift_show_rentals/+1')
    rental_button = InlineKeyboardButton(text=f"{rental_number}/{total_rentals} Расписание",
                                         callback_data=f"schedule {rental_number}")
    if rental_number == 1:
        kb_builder.row(rental_button, forward_btn)
    elif rental_number == total_rentals:
        kb_builder.row(backward_btn, rental_button)
    else:
        kb_builder.row(backward_btn, rental_button, forward_btn)
    return kb_builder.as_markup()

def create_slot_pagination_keyboard(slot_number, total_slots) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    backward_btn = InlineKeyboardButton(text='<<', callback_data='shift_show_slots/-1')
    forward_btn = InlineKeyboardButton(text='>>', callback_data='shift_show_slots/+1')
    sign_up_button = InlineKeyboardButton(text=f"Записаться",
                                         callback_data=f"sign_up_slot {slot_number}")
    if slot_number == 1:
        kb_builder.row(sign_up_button, forward_btn)
    elif slot_number == total_slots:
        kb_builder.row(backward_btn, sign_up_button)
    else:
        kb_builder.row(backward_btn, sign_up_button, forward_btn)
    return kb_builder.as_markup()

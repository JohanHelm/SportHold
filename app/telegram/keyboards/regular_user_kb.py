from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class RentalsCallbackFactory(CallbackData, prefix="rentals"):
    step: int


forward_callback_data = RentalsCallbackFactory(step=1).pack()
back_callback_data = RentalsCallbackFactory(step=-1).pack()


def create_first_regular_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    show_rentals_btn = InlineKeyboardButton(
        text="Объекты!", callback_data="show_rentals"
    )
    kb_builder.row(show_rentals_btn)
    return kb_builder.as_markup()


def create_rental_pagination_keyboard(db_offset, rental_count) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    backward_btn = InlineKeyboardButton(text="<<", callback_data=back_callback_data)
    forward_btn = InlineKeyboardButton(text=">>", callback_data=forward_callback_data)
    main_menu_btn = InlineKeyboardButton(text="В меню", callback_data="to_main_menu")
    new_sign_up_button = InlineKeyboardButton(
        text=f"{db_offset}/{rental_count} Новое бронирование",
        callback_data="new_booking",
    )

    if db_offset == 1:
        kb_builder.row(new_sign_up_button)
        kb_builder.row(main_menu_btn, forward_btn)
    elif db_offset == rental_count:
        kb_builder.row(new_sign_up_button)
        kb_builder.row(main_menu_btn, backward_btn)
    else:
        kb_builder.row(new_sign_up_button)
        kb_builder.row(main_menu_btn, backward_btn, forward_btn)
    return kb_builder.as_markup()


def create_slot_pagination_keyboard(
    slots, slot_page, total_slots, slots_per_page
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for index, slot in enumerate(slots):
        slot_start_time = slot.started.strftime("%H:%M")
        slot_end_time = slot.ended.strftime("%H:%M")
        btn_text = f"{slot_start_time} - {slot_end_time} Свободно!"
        slot_btn = InlineKeyboardButton(
            text=btn_text, callback_data=f"book_in_slot {index}"
        )
        kb_builder.row(slot_btn)
    backward_btn = InlineKeyboardButton(text="<<", callback_data="shift_show_slots/-1")
    forward_btn = InlineKeyboardButton(text=">>", callback_data="shift_show_slots/+1")
    main_menu_btn = InlineKeyboardButton(text="В меню", callback_data="to_main_menu")
    back_to_rentals_btn = InlineKeyboardButton(
        text="К списку объектов", callback_data="back_to_rentals"
    )
    if slot_page == 0:
        kb_builder.row(back_to_rentals_btn)
        kb_builder.row(main_menu_btn, forward_btn)
    elif (slot_page + 1) * slots_per_page >= total_slots:
        kb_builder.row(back_to_rentals_btn)
        kb_builder.row(main_menu_btn, backward_btn)
    else:
        kb_builder.row(back_to_rentals_btn)
        kb_builder.row(main_menu_btn, backward_btn, forward_btn)
    return kb_builder.as_markup()

import locale
from datetime import date, timedelta
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.infra.db.models.record.schema import Record
from app.telegram.context.querys import Book, Nav, Records, RentalQuerys
from app.telegram.context.states import FSMRegularUser
from app.telegram.context.callbacks import back_callback_data, forward_callback_data

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

BTN_GO_TO_MAIN = InlineKeyboardButton(text="В меню", callback_data=Nav.TO_MAIN)
BTN_BACK_TO_RENTALS = InlineKeyboardButton(
    text="К списку объектов", callback_data=RentalQuerys.BACK
)


def create_first_regular_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    show_rentals_btn = InlineKeyboardButton(
        text="Доступные объекты!", callback_data=RentalQuerys.SHOW_RENTALS
    )
    user_records_btn = InlineKeyboardButton(
        text="Мои записи", callback_data=Records.SHOW_RECORDS
    )
    kb_builder.row(show_rentals_btn, user_records_btn)
    return kb_builder.as_markup()


def create_rental_pagination_keyboard(db_offset, rental_count) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    backward_btn = InlineKeyboardButton(text="<<", callback_data=back_callback_data)
    forward_btn = InlineKeyboardButton(text=">>", callback_data=forward_callback_data)
    select_booking_date_btn = InlineKeyboardButton(
        text="К выбору даты записи.",
        callback_data=Book.SELECT_BOOK_DAY,
    )
    kb_builder.row(select_booking_date_btn)
    if db_offset == 1:
        kb_builder.row(BTN_GO_TO_MAIN, forward_btn)
    elif db_offset == rental_count:
        kb_builder.row(BTN_GO_TO_MAIN, backward_btn)
    else:
        kb_builder.row(BTN_GO_TO_MAIN, backward_btn, forward_btn)
    return kb_builder.as_markup()


def create_date_pagination_keyboard(
    current_date, days_to_book_in
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    date_buttons: list[InlineKeyboardButton] = []
    date_range = [
        date.fromordinal(_)
        for _ in range(
            current_date.toordinal(),
            (current_date + timedelta(days=days_to_book_in)).toordinal(),
        )
    ]
    for day in date_range:
        button_text = day.strftime("%d.%m.%Y г.")
        date_buttons.append(
            InlineKeyboardButton(text=button_text, callback_data=f"booking_date/{day}")
        )
    kb_builder.row(*date_buttons, width=3)
    kb_builder.row(BTN_BACK_TO_RENTALS)
    kb_builder.row(BTN_GO_TO_MAIN)
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
    kb_builder.row(BTN_BACK_TO_RENTALS)
    if slot_page == 0:
        kb_builder.row(BTN_GO_TO_MAIN, forward_btn)
    elif (slot_page + 1) * slots_per_page >= total_slots:
        kb_builder.row(BTN_GO_TO_MAIN, backward_btn)
    else:
        kb_builder.row(BTN_GO_TO_MAIN, backward_btn, forward_btn)
    return kb_builder.as_markup()


async def create_user_records_keyboard(
    user_records_to_rental: list[Record],
    state: FSMContext,
    rental_with_record_num: int,
    rentals_with_user_records_amount: int,
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for record in user_records_to_rental:
        record_date = record.slot.started.strftime("%d %B %Y")
        record_start_time = record.slot.started.strftime("%H:%M")
        record_end_time = record.slot.ended.strftime("%H:%M")
        btn_text = f"{record_date}. {record_start_time} - {record_end_time}. Удалить"
        record_btn = InlineKeyboardButton(
            text=btn_text, callback_data=f"delete_record/{record.id}/{record.slot_id}"
        )
        kb_builder.row(record_btn)
    user_state = await state.get_state()
    if user_state == FSMRegularUser.choosing_slot_page:
        to_previous_rental = InlineKeyboardButton(
            text="К последнему объекту", callback_data="to_previous_slots_page"
        )
        kb_builder.row(BTN_BACK_TO_RENTALS)
        kb_builder.row(to_previous_rental)
    backward_btn = InlineKeyboardButton(
        text="<<", callback_data="shift_user_records/-1"
    )
    forward_btn = InlineKeyboardButton(text=">>", callback_data="shift_user_records/+1")
    if rentals_with_user_records_amount <= 1:
        kb_builder.row(BTN_GO_TO_MAIN)
    elif rental_with_record_num == 0 and rentals_with_user_records_amount > 1:
        kb_builder.row(BTN_GO_TO_MAIN, forward_btn)
    elif (
        rental_with_record_num + 1 == rentals_with_user_records_amount
        and rentals_with_user_records_amount > 1
    ):
        kb_builder.row(BTN_GO_TO_MAIN, backward_btn)
    else:
        kb_builder.row(BTN_GO_TO_MAIN, backward_btn, forward_btn)
    return kb_builder.as_markup()

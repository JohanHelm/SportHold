from datetime import date, timedelta, datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.domain.models.slot.dto import SlotData
from app.domain.controllers.slots import SlotManager
from app.telegram.context.querys import Book
from app.telegram.context.states import FSMRegularUser

from app.telegram.keyboards.regular_user_kb import (
    create_slot_pagination_keyboard,
    create_date_pagination_keyboard,
)

from app.telegram.messages.text_messages import (
    display_booking_info,
    display_date_selection_info,
)

from app.telegram.utils.db_queries import (
    get_rental_book_policy,
    get_rental_with_suitable_schedules,
    get_occupied_slots,
)

router: Router = Router()


@router.callback_query(
    F.data == Book.SELECT_BOOK_DAY, StateFilter(FSMRegularUser.choosing_rental_number)
)
async def select_booking_date(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = (await state.get_data())["db_offset"]
    await state.set_state(FSMRegularUser.choosing_booking_date)
    current_rental, _ = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    policy = await get_rental_book_policy(db_session=db_session, db_offset=db_offset)
    # TODO: добавить поле в Policy
    avaiable_first_book_day = date.today() + timedelta(days=1)
    await callback.message.edit_text(
        text=display_date_selection_info(current_rental),
        reply_markup=create_date_pagination_keyboard(
            avaiable_first_book_day, policy.book_limit_days
        ),
    )


@router.callback_query(
    F.data.startswith("booking_date"), StateFilter(FSMRegularUser.choosing_booking_date)
)
async def show_rentals_slots(callback: CallbackQuery, state: FSMContext, db_session):
    selected_date = datetime.strptime(callback.data.split("/")[1], "%Y-%m-%d").date()
    await state.update_data(choosing_booking_date=selected_date)
    db_offset = (await state.get_data())["db_offset"]

    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    occupied_slots = await get_occupied_slots(db_session, current_rental, selected_date)
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(
        current_rental_schedules,
        occupied_slots,
        date=selected_date,
    )
    await state.set_state(FSMRegularUser.choosing_slot_page)
    slot_page = 0
    await state.update_data(choosing_slot_page=slot_page)
    # TODO Сейчас параметр slots_per_page хардкод, в перспективе надо вынеси его в настройки объекта для оунера
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(
        text=display_booking_info(current_rental_schedules[0], selected_date),
        reply_markup=create_slot_pagination_keyboard(
            slots.slots[start_slice:end_slice],
            slot_page,
            len(slots.slots),
            slots_per_page,
        ),
    )

from datetime import date, datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.domain.models.slot.dto import SlotModel, SlotData
from app.domain.controllers.slots import SlotManager

from app.telegram.keyboards.regular_user_kb import (
    RentalsCallbackFactory,
    create_rental_pagination_keyboard,
    create_slot_pagination_keyboard,
    create_first_regular_keyboard,
    create_user_records_keyboard,
    create_user_records_simple_keyboard,
)

from app.telegram.messages.text_messages import (
    display_rental_info,
    display_booking_info,
    hello_regular_user,
    no_rentals_in_db,
    display_user_records,
)

from app.telegram.utils.db_queries import (
    get_rental_with_suitable_schedules,
    get_rentals_for_user_count,
    get_records_for_user_count,
    create_slot_in_db,
    create_record_in_db,
    get_user_records,
)

router: Router = Router()


class ShowRentalSlots(StatesGroup):
    choosing_rental_number = State()
    choosing_slot_page = State()


@router.callback_query(F.data == "show_rentals", StateFilter(None))
async def show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = 0
    await state.set_state(ShowRentalSlots.choosing_rental_number)
    await state.update_data(db_offset=db_offset)
    rental_for_user_count = await get_rentals_for_user_count(db_session=db_session)
    if rental_for_user_count:
        (
            current_rental,
            current_rental_schedules,
        ) = await get_rental_with_suitable_schedules(
            db_session=db_session, db_offset=db_offset
        )
        await callback.message.edit_text(
            text=display_rental_info(current_rental, current_rental_schedules),
            reply_markup=create_rental_pagination_keyboard(
                db_offset + 1, rental_for_user_count
            ),
        )
    else:
        await callback.message.edit_text(
            text=no_rentals_in_db(rental_for_user_count, rental_for_user_count),
            reply_markup=create_first_regular_keyboard(),
        )


@router.callback_query(F.data == "show_user_records")
async def show_user_records(callback: CallbackQuery, db_session):
    user_records = await get_user_records(db_session, callback.from_user.id)
    await callback.message.edit_text(
        text=display_user_records(),
        reply_markup=create_user_records_simple_keyboard(user_records))


@router.callback_query(
    RentalsCallbackFactory.filter(),
    StateFilter(ShowRentalSlots.choosing_rental_number),
)
async def shift_show_rentals(
    callback: CallbackQuery,
    state: FSMContext,
    db_session,
    callback_data: RentalsCallbackFactory,
):
    db_offset = (await state.get_data())["db_offset"] + callback_data.step
    await state.update_data(db_offset=db_offset)
    rental_count = await get_rentals_for_user_count(db_session=db_session)
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    await callback.message.edit_text(
        text=display_rental_info(current_rental, current_rental_schedules),
        reply_markup=create_rental_pagination_keyboard(db_offset + 1, rental_count),
    )


@router.callback_query(
    F.data == "new_booking", StateFilter(ShowRentalSlots.choosing_rental_number)
)
async def show_rentals_slots(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = (await state.get_data())["db_offset"]

    _, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )

    current_date = datetime.today()
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(
        current_rental_schedules, date=current_date
    )
    await state.set_state(ShowRentalSlots.choosing_slot_page)
    slot_page = 0
    await state.update_data(choosing_slot_page=slot_page)
    # TODO Сейчас параметр slots_per_page хардкод, в перспективе надо вынеси его в настройки объекта для оунера
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(
        text=display_booking_info(current_rental_schedules[0]),
        reply_markup=create_slot_pagination_keyboard(
            slots.slots[start_slice:end_slice],
            slot_page,
            len(slots.slots),
            slots_per_page,
        ),
    )


@router.callback_query(
    F.data.startswith("shift_show_slots"),
    StateFilter(ShowRentalSlots.choosing_slot_page),
)
async def shift_show_rentals_slots(
    callback: CallbackQuery, state: FSMContext, db_session
):
    slot_page = (await state.get_data())["choosing_slot_page"] + int(
        callback.data.split("/")[1]
    )
    await state.update_data(choosing_slot_page=slot_page)
    db_offset = (await state.get_data())["db_offset"]
    _, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    current_date = datetime.today()
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(current_rental_schedules, date=current_date)
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(
        text=display_booking_info(current_rental_schedules[0]),
        reply_markup=create_slot_pagination_keyboard(
            slots.slots[start_slice:end_slice],
            slot_page,
            len(slots.slots),
            slots_per_page,
        ),
    )


@router.callback_query(
    F.data.startswith("book_in_slot"), StateFilter(ShowRentalSlots.choosing_slot_page)
)
async def book_in_slot(callback: CallbackQuery, state: FSMContext, db_session):
    slot_number = int(callback.data.split()[1])
    slot_page = (await state.get_data())["choosing_slot_page"]
    db_offset = (await state.get_data())["db_offset"]
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    current_date = datetime.today()
    manager = SlotManager()
    slots = manager.generate_time_intervals(current_rental_schedules, date=current_date)
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    choosen_slot: SlotModel = slots.slots[start_slice:end_slice][slot_number]
    new_slot = await create_slot_in_db(db_session, current_rental, choosen_slot)
    await create_record_in_db(db_session, callback.from_user.id, new_slot, current_rental)
    user_records = await get_user_records(db_session, callback.from_user.id)
    await callback.message.edit_text(
        text=display_user_records(),
        reply_markup=create_user_records_keyboard(user_records),
    )


@router.callback_query(
    F.data.startswith("to_previous_slots_page"), StateFilter(ShowRentalSlots.choosing_slot_page)
)
async def to_previous_slots_page(callback: CallbackQuery, state: FSMContext, db_session):
    slot_page = (await state.get_data())["choosing_slot_page"]
    db_offset = (await state.get_data())["db_offset"]
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    current_date = datetime.today()
    manager = SlotManager()
    slots = manager.generate_time_intervals(current_rental_schedules, date=current_date)
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(
        text=display_booking_info(current_rental_schedules[0]),
        reply_markup=create_slot_pagination_keyboard(
            slots.slots[start_slice:end_slice],
            slot_page,
            len(slots.slots),
            slots_per_page,
        ),
    )


@router.callback_query(
    F.data.startswith("back_to_rentals"),
    StateFilter(ShowRentalSlots.choosing_slot_page),
)
async def back_to_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = (await state.get_data())["db_offset"]
    await state.set_state(ShowRentalSlots.choosing_rental_number)

    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    rental_for_user_count = await get_rentals_for_user_count(db_session=db_session)
    await callback.message.edit_text(
        text=display_rental_info(current_rental, current_rental_schedules),
        reply_markup=create_rental_pagination_keyboard(
            db_offset + 1, rental_for_user_count
        ),
    )


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu(callback: CallbackQuery, state: FSMContext, db_session):
    await state.clear()
    available_rentals: int = await get_rentals_for_user_count(db_session=db_session)
    total_rentals = available_rentals
    records_amount: int = await get_records_for_user_count(db_session, callback.from_user.id)
    await callback.message.edit_text(
        hello_regular_user(
            callback.from_user.username, available_rentals, total_rentals, records_amount
        ),
        reply_markup=create_first_regular_keyboard(),
    )

from datetime import date, timedelta, datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.domain.models.slot.dto import SlotModel, SlotData
from app.domain.controllers.slots import SlotManager
from app.telegram.context.states import FSMRegularUser

from app.telegram.keyboards.regular_user_kb import (
    create_rental_pagination_keyboard,
    create_slot_pagination_keyboard,
    create_first_regular_keyboard,
    create_user_records_keyboard,
    create_date_pagination_keyboard,
)

from app.telegram.messages.text_messages import (
    display_rental_info,
    display_booking_info,
    hello_regular_user,
    no_rentals_in_db,
    display_user_records,
    display_date_selection_info,
)

from app.telegram.utils.db_queries import (
    get_rental_with_suitable_schedules,
    get_rentals_for_user_count,
    get_records_for_user_count,
    create_slot_in_db,
    create_record_in_db,
    delete_user_record,
    delete_slot_by_id,
    get_rentals_with_user_records,
    get_user_records_to_rental,
    get_occupied_slots,
)

router: Router = Router()


@router.callback_query(F.data == "show_user_records", StateFilter(None))
async def show_user_records(callback: CallbackQuery, state: FSMContext, db_session):
    rental_with_record_num = 0
    await state.update_data(rental_with_record=rental_with_record_num)
    rentals_with_user_records = await get_rentals_with_user_records(db_session, callback.from_user.id)
    if rentals_with_user_records:
        user_records_to_rental = await get_user_records_to_rental(
            db_session,
            callback.from_user.id,
            rentals_with_user_records[rental_with_record_num])
    else:
        user_records_to_rental = ()

    await callback.message.edit_text(
        text=display_user_records(user_records_to_rental),
        reply_markup=await create_user_records_keyboard(
            user_records_to_rental,
            state,
            rental_with_record_num,
            len(rentals_with_user_records)))


@router.callback_query(
    F.data == "select_booking_date", StateFilter(FSMRegularUser.choosing_rental_number)
)
async def select_booking_date(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = (await state.get_data())["db_offset"]
    await state.set_state(FSMRegularUser.choosing_booking_date)
    current_rental, _ = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    # Запись возможна с завтрашнего дня!!!
    current_date = date.today() + timedelta(days=1)
    await callback.message.edit_text(
        text=display_date_selection_info(current_rental),
        reply_markup=create_date_pagination_keyboard(current_date, current_rental.days_to_book_in),
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
        current_rental_schedules, occupied_slots, date=selected_date,
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


@router.callback_query(
    F.data.startswith("shift_show_slots"),
    StateFilter(FSMRegularUser.choosing_slot_page),
)
async def shift_show_rentals_slots(
    callback: CallbackQuery, state: FSMContext, db_session
):
    slot_page = (await state.get_data())["choosing_slot_page"] + int(
        callback.data.split("/")[1]
    )
    await state.update_data(choosing_slot_page=slot_page)
    db_offset = (await state.get_data())["db_offset"]
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    selected_date = (await state.get_data())["choosing_booking_date"]
    occupied_slots = await get_occupied_slots(db_session, current_rental, selected_date)
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(current_rental_schedules, occupied_slots, date=selected_date)
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


@router.callback_query(
    F.data.startswith("book_in_slot"), StateFilter(FSMRegularUser.choosing_slot_page)
)
async def book_in_slot(callback: CallbackQuery, state: FSMContext, db_session):
    slot_number = int(callback.data.split()[1])
    slot_page = (await state.get_data())["choosing_slot_page"]
    db_offset = (await state.get_data())["db_offset"]
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    selected_date = (await state.get_data())["choosing_booking_date"]
    occupied_slots = await get_occupied_slots(db_session, current_rental, selected_date)
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(current_rental_schedules, occupied_slots, date=selected_date)
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    choosen_slot: SlotModel = slots.slots[start_slice:end_slice][slot_number]
    new_slot = await create_slot_in_db(db_session, current_rental, choosen_slot)
    await create_record_in_db(db_session, callback.from_user.id, new_slot, current_rental)

    rental_with_record_num = db_offset
    await state.update_data(rental_with_record=rental_with_record_num)
    rentals_with_user_records = await get_rentals_with_user_records(db_session, callback.from_user.id)
    user_records_to_rental = await get_user_records_to_rental(
        db_session,
        callback.from_user.id,
        current_rental.id)

    await callback.message.edit_text(
        text=display_user_records(user_records_to_rental),
        reply_markup=await create_user_records_keyboard(
            user_records_to_rental,
            state,
            rental_with_record_num,
            len(rentals_with_user_records)))


@router.callback_query(
    F.data.startswith("delete_record"),
    StateFilter(FSMRegularUser.choosing_slot_page, default_state)
)
async def delete_record(callback: CallbackQuery, state: FSMContext, db_session):
    await delete_user_record(db_session, int(callback.data.split("/")[1]))
    # TODO при реализации множественной записи в один слот здесь нужно будет удалять запись из слота
    await delete_slot_by_id(db_session, int(callback.data.split("/")[2]))
    rental_with_record_num = (await state.get_data())["rental_with_record"]
    rentals_with_user_records = await get_rentals_with_user_records(db_session, callback.from_user.id)
    if rentals_with_user_records:
        user_records_to_rental = await get_user_records_to_rental(
            db_session,
            callback.from_user.id,
            rentals_with_user_records[rental_with_record_num])
    else:
        user_records_to_rental = ()
    await callback.message.edit_text(
        text=display_user_records(user_records_to_rental),
        reply_markup=await create_user_records_keyboard(
            user_records_to_rental,
            state,
            rental_with_record_num,
            len(rentals_with_user_records)))


@router.callback_query(
    F.data.startswith("shift_user_records"),
    StateFilter(FSMRegularUser.choosing_slot_page, default_state)
)
async def shift_show_user_records(callback: CallbackQuery, state: FSMContext, db_session):
    rental_with_record_num = (await state.get_data())["rental_with_record"] + int(callback.data.split("/")[1])
    await state.update_data(rental_with_record=rental_with_record_num)
    rentals_with_user_records = await get_rentals_with_user_records(db_session, callback.from_user.id)
    user_records_to_rental = await get_user_records_to_rental(
        db_session,
        callback.from_user.id,
        rentals_with_user_records[rental_with_record_num])
    await callback.message.edit_text(
        text=display_user_records(user_records_to_rental),
        reply_markup=await create_user_records_keyboard(
            user_records_to_rental,
            state,
            rental_with_record_num,
            len(rentals_with_user_records)))


@router.callback_query(
    F.data == "to_previous_slots_page", StateFilter(FSMRegularUser.choosing_slot_page)
)
async def to_previous_slots_page(callback: CallbackQuery, state: FSMContext, db_session):
    slot_page = (await state.get_data())["choosing_slot_page"]
    db_offset = (await state.get_data())["db_offset"]
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    selected_date = (await state.get_data())["choosing_booking_date"]
    occupied_slots = await get_occupied_slots(db_session, current_rental, selected_date)
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(current_rental_schedules, occupied_slots, date=selected_date)
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


@router.callback_query(
    F.data == "back_to_rentals",
    StateFilter(FSMRegularUser.choosing_slot_page),
)
async def back_to_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = (await state.get_data())["db_offset"]
    await state.set_state(FSMRegularUser.choosing_rental_number)

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

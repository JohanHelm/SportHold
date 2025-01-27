from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.domain.models.slot.dto import SlotModel, SlotData
from app.domain.controllers.slots import SlotManager
from app.telegram.context.states import FSMRegularUser

from app.telegram.keyboards.regular_user_kb import (
    create_slot_pagination_keyboard,
    create_user_records_keyboard,
)

from app.telegram.messages.text_messages import (
    display_booking_info,
    display_user_records,
)

from app.telegram.utils.db_queries import (
    get_rental_with_suitable_schedules,
    create_slot_in_db,
    create_record_in_db,
    get_rentals_with_user_records,
    get_user_records_to_rental,
    get_occupied_slots,
)

router: Router = Router()



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
    slots: SlotData = manager.generate_time_intervals(
        current_rental_schedules, occupied_slots, date=selected_date
    )
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
    slots: SlotData = manager.generate_time_intervals(
        current_rental_schedules, occupied_slots, date=selected_date
    )
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    choosen_slot: SlotModel = slots.slots[start_slice:end_slice][slot_number]
    new_slot = await create_slot_in_db(db_session, current_rental, choosen_slot)
    await create_record_in_db(
        db_session, callback.from_user.id, new_slot, current_rental
    )

    rental_with_record_num = db_offset
    await state.update_data(rental_with_record=rental_with_record_num)
    rentals_with_user_records = await get_rentals_with_user_records(
        db_session, callback.from_user.id
    )
    user_records_to_rental = await get_user_records_to_rental(
        db_session, callback.from_user.id, current_rental.id
    )

    await callback.message.edit_text(
        text=display_user_records(user_records_to_rental),
        reply_markup=await create_user_records_keyboard(
            user_records_to_rental,
            state,
            rental_with_record_num,
            len(rentals_with_user_records),
        ),
    )


@router.callback_query(
    F.data == "to_previous_slots_page", StateFilter(FSMRegularUser.choosing_slot_page)
)
async def to_previous_slots_page(
    callback: CallbackQuery, state: FSMContext, db_session
):
    slot_page = (await state.get_data())["choosing_slot_page"]
    db_offset = (await state.get_data())["db_offset"]
    current_rental, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )
    selected_date = (await state.get_data())["choosing_booking_date"]
    occupied_slots = await get_occupied_slots(db_session, current_rental, selected_date)
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(
        current_rental_schedules, occupied_slots, date=selected_date
    )
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


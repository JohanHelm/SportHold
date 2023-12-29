from datetime import date, datetime
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from aiogram import Router, F
from aiogram.types import CallbackQuery

from loguru import logger

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.domain.helpers.enums import ScheduleStatus
from app.infra.db.models.schedule.schema import Schedule

from app.telegram.keyboards.regular_user_kb import (
    RentalsCallbackFactory,
    create_rental_pagination_keyboard,
    create_slot_pagination_keyboard,
    create_first_regular_keyboard,
)
from app.domain.controllers.slots import SlotManager
from app.telegram.messages.text_messages import (
    display_rental_info,
    display_booking_info,
    hello_regular_user,
    no_rentals_in_db,
)
from app.infra.db.models.rental.schema import Rental
from app.domain.models.slot.dto import SlotModel, SlotData

router: Router = Router()


async def get_rentals_for_user_count(db_session) -> int:
    async with db_session() as session:
        rental_count = await session.scalar(select(func.count(Rental.id)))
        return rental_count


async def get_rental_with_suitable_schedules(db_session, db_offset):
    async with db_session() as session:
        row_rental = await session.execute(
            select(Rental).group_by(Rental.id).offset(db_offset).limit(1)
        )
        current_rental = row_rental.scalar()

        rows_schedules = await session.execute(
            select(Schedule)
            .where(Schedule.rental_id == current_rental.id)
            .where(Schedule.status == ScheduleStatus.ACTIVE)
            .order_by(Schedule.slot_type)
        )

        current_rental_schedules = rows_schedules.scalars().all()
        logger.debug(current_rental_schedules)
        return current_rental, current_rental_schedules


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
            reply_markup=create_rental_pagination_keyboard(db_offset + 1, rental_for_user_count),
        )
    else:
        await callback.message.edit_text(
            text=no_rentals_in_db(rental_for_user_count, rental_for_user_count),
            reply_markup=create_first_regular_keyboard(),
        )


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
    db_offset = (await state.get_data())["db_offset"] + (callback_data.step)
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

    date = datetime.today()
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(current_rental_schedules, date=date)
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
    # async with db_session() as session:
    #     result = await session.execute(
    #         select(Rental).options(selectinload(Rental.schedules))
    #     )
    #     rentals = result.scalars().all()
    #     rental_number = (await state.get_data())["choosing_rental_number"]
    #     rentals_schedules = rentals[rental_number].schedules
    db_offset = (await state.get_data())["db_offset"]
    _, current_rental_schedules = await get_rental_with_suitable_schedules(
        db_session=db_session, db_offset=db_offset
    )

    date = datetime.today()
    manager = SlotManager()
    slots = manager.generate_time_intervals(current_rental_schedules, date=date)
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


# @router.callback_query(F.data.startswith('sign_up_to_slot'), StateFilter(ShowRentalSlots.choosing_slot_number))
# async def sign_up_to_slot(callback: CallbackQuery, state: FSMContext, db_session):
#     slot_number = (await state.get_data())['choosing_slot_number']
#     rental = RentalDAO()
#     rentals = await rental.show_rentals(db_session)
#     rental_number = (await state.get_data())['choosing_rental_number']
#     rental_id = rentals[rental_number].rental_id
#     schedule = ScheduleDAO()
#     rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)
#     date = datetime.today()
#     manager = ScheduleManager()
#     slots = manager.generate_time_intervals(rentals_schedules, date=date)
#     user_id = callback.from_user.id
#     # slot_id = slots[slot_number].slot_id
#     # Создать слот в базе
#     # Cоздать рекорд в базе
#
#     await callback.message.edit_text(text=str(user_id))


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

    # async with db_session() as session:
    #     result = await session.execute(
    #         select(Rental).options(selectinload(Rental.schedules))
    #     )
    #     rentals = result.scalars().all()
    #     rentals_schedules = rentals[rental_number].schedules

    rental_for_user_count = await get_rentals_for_user_count(db_session=db_session)

    await callback.message.edit_text(
        text=display_rental_info(current_rental, current_rental_schedules),
        reply_markup=create_rental_pagination_keyboard(db_offset + 1, rental_for_user_count),
    )


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu(callback: CallbackQuery, state: FSMContext, db_session):
    await state.clear()
    avalable_rentals: int = 2
    total_rentals: int = 2
    records_amount: int = 0
    await callback.message.edit_text(
        hello_regular_user(
            callback.from_user.username, avalable_rentals, total_rentals, records_amount
        ),
        reply_markup=create_first_regular_keyboard(),
    )

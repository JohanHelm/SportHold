from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.telegram.keyboards.regular_user_kb import (
    create_rental_pagination_keyboard,
    create_slot_pagination_keyboard,
    create_first_regular_keyboard,
)
from app.domain.controllers.slots import SlotManager
from app.telegram.messages.text_messages import (
    display_rental_info,
    display_booking_info,
    hello_regular_user,
)
from app.infra.db.models.rental.schema import Rental
from app.domain.models.slot.dto import SlotModel, SlotData

router: Router = Router()


class ShowRentalSlots(StatesGroup):
    choosing_rental_number = State()
    choosing_slot_page = State()


@router.callback_query(F.data == "show_rentals", StateFilter(None))
async def show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    await state.set_state(ShowRentalSlots.choosing_rental_number)
    rental_number = 0
    await state.update_data(choosing_rental_number=rental_number)
    # TODO: предлагаю пагинацию делать через offset\limit в запросе с order_by по rental.id
    # TODO: т.е. мы отсортировываем по возрастанию ID и с помощью оффсета смещаем SELECT
    # TODO: таким образом у нас не нарушится порядок, в котором мы показываем объекты
    # TODO: соот-но в состояние можно хранить инфо про текущий offset и count объектов
    async with db_session() as session:
        # TODO: Объектов в базе может и не быть, необходимо эту логику проработать
        result = await session.execute(
            select(Rental).options(selectinload(Rental.schedules))
        )
        rentals = result.scalars().all()
        # TODO: а что если объект добавлен, но у него нет ни одного расписания или ни одного активного расписания?
        # TODO: Или нет расписаний, которые на данный момент действуют - started < now() < ended ?
        rentals_schedules = rentals[rental_number].schedules
    # TODO Переписать display_rental_info чтобы принимала список расписаний и выводила рабочее время и перерывы.
    # TODO тут должна быть какая то логика, если активных расписаний нет
    # TODO предполагаю, что в display_rental_info уйдеи список активных расписаний, действующих на текущий момент
    await callback.message.edit_text(
        text=display_rental_info(rentals[rental_number], rentals_schedules[0]),
        reply_markup=create_rental_pagination_keyboard(rental_number + 1, len(rentals)),
    )


@router.callback_query(
    F.data.startswith("shift_show_rentals"),
    StateFilter(ShowRentalSlots.choosing_rental_number),
)
async def shift_show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())["choosing_rental_number"] + int(
        callback.data.split("/")[1]
    )
    await state.update_data(choosing_rental_number=rental_number)
    async with db_session() as session:
        result = await session.execute(
            select(Rental).options(selectinload(Rental.schedules))
        )
        rentals = result.scalars().all()
        rentals_schedules = rentals[rental_number].schedules
    await callback.message.edit_text(
        text=display_rental_info(rentals[rental_number], rentals_schedules[0]),
        reply_markup=create_rental_pagination_keyboard(rental_number + 1, len(rentals)),
    )


@router.callback_query(
    F.data == "new_booking", StateFilter(ShowRentalSlots.choosing_rental_number)
)
async def show_rentals_slots(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())["choosing_rental_number"]
    async with db_session() as session:
        result = await session.execute(
            select(Rental).options(selectinload(Rental.schedules))
        )
        rentals = result.scalars().all()
        rentals_schedules = rentals[rental_number].schedules
    date = datetime.today()
    manager = SlotManager()
    slots: SlotData = manager.generate_time_intervals(rentals_schedules, date=date)
    await state.set_state(ShowRentalSlots.choosing_slot_page)
    slot_page = 0
    await state.update_data(choosing_slot_page=slot_page)
    # TODO Сейчас параметр slots_per_page хардкод, в перспективе надо вынеси его в настройки объекта для оунера
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(
        text=display_booking_info(rentals_schedules[0]),
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
    async with db_session() as session:
        result = await session.execute(
            select(Rental).options(selectinload(Rental.schedules))
        )
        rentals = result.scalars().all()
        rental_number = (await state.get_data())["choosing_rental_number"]
        rentals_schedules = rentals[rental_number].schedules
    date = datetime.today()
    manager = SlotManager()
    slots = manager.generate_time_intervals(rentals_schedules, date=date)
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(
        text=display_booking_info(rentals_schedules[0]),
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
    rental_number = (await state.get_data())["choosing_rental_number"]
    await state.set_state(ShowRentalSlots.choosing_rental_number)
    async with db_session() as session:
        result = await session.execute(
            select(Rental).options(selectinload(Rental.schedules))
        )
        rentals = result.scalars().all()
        rentals_schedules = rentals[rental_number].schedules
    await callback.message.edit_text(
        text=display_rental_info(rentals[rental_number], rentals_schedules[0]),
        reply_markup=create_rental_pagination_keyboard(rental_number + 1, len(rentals)),
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

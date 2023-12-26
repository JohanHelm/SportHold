from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from app.domain.controllers.schedules import ScheduleManager
from app.infra.db.models.rental.dao import RentalDAO
from app.infra.db.models.schedule.dao import ScheduleDAO
from app.infra.db.models.slot.dao import SlotDAO
from app.domain.models.slot.dto import SlotCreate, SlotStatus, SlotType
from app.telegram.keyboards.regular_user_kb import \
    create_rental_pagination_keyboard, \
    create_slot_pagination_keyboard, \
    create_first_regular_keyboard
from app.telegram.messages.text_messages import display_rental_info, display_booking_info, hello_regular_user

router: Router = Router()


class ShowRentalSlots(StatesGroup):
    choosing_rental_number = State()
    choosing_slot_page = State()


# Возможно добавить опрос юзверя, типа напиши своё имя, номер телефона для связи, и т п
class SignUpToSlot(StatesGroup):
    fill_name = State()
    fill_phone = State()


@router.callback_query(F.data == 'show_rentals')  # , StateFilter(None))
async def show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    await state.set_state(ShowRentalSlots.choosing_rental_number)
    rental_number = 0
    await state.update_data(choosing_rental_number=rental_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)
    # TODO rentals_schedules должен содержать не список всех расписаний объекта,
    #  а активное на данный момент или на искомый день расписание.
    await callback.message.edit_text(text=display_rental_info(rentals[rental_number], rentals_schedules[0]),
                                     reply_markup=create_rental_pagination_keyboard(rental_number + 1, len(rentals)))


@router.callback_query(F.data.startswith('shift_show_rentals'), StateFilter(ShowRentalSlots.choosing_rental_number))
async def shift_show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())['choosing_rental_number'] + int(callback.data.split('/')[1])
    await state.update_data(choosing_rental_number=rental_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)

    await callback.message.edit_text(text=display_rental_info(rentals[rental_number], rentals_schedules[0]),
                                     reply_markup=create_rental_pagination_keyboard(rental_number + 1, len(rentals)))


@router.callback_query(F.data == "new_booking", StateFilter(ShowRentalSlots.choosing_rental_number))
async def show_rentals_slots(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())['choosing_rental_number']
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)
    date = datetime.today()
    manager = ScheduleManager()
    slots = manager.generate_time_intervals(rentals_schedules, date=date)
    await state.set_state(ShowRentalSlots.choosing_slot_page)
    slot_page = 0
    await state.update_data(choosing_slot_page=slot_page)
    # TODO Сейчас параметр slots_per_page хардкод, в перспективе надо вынеси его в настройки объекта для оунера
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(text=display_booking_info(rentals_schedules[0]),
                                     reply_markup=create_slot_pagination_keyboard(slots[start_slice:end_slice],
                                                                                  slot_page, len(slots),
                                                                                  slots_per_page))


@router.callback_query(F.data.startswith('shift_show_slots'), StateFilter(ShowRentalSlots.choosing_slot_page))
async def shift_show_rentals_slots(callback: CallbackQuery, state: FSMContext, db_session):
    slot_page = (await state.get_data())['choosing_slot_page'] + int(callback.data.split('/')[1])
    await state.update_data(choosing_slot_page=slot_page)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_number = (await state.get_data())['choosing_rental_number']
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)
    date = datetime.today()
    manager = ScheduleManager()
    slots = manager.generate_time_intervals(rentals_schedules, date=date)
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    await callback.message.edit_text(text=display_booking_info(rentals_schedules[0]),
                                     reply_markup=create_slot_pagination_keyboard(slots[start_slice:end_slice],
                                                                                  slot_page, len(slots),
                                                                                  slots_per_page))


@router.callback_query(F.data.startswith('sign_up_to_slot'), StateFilter(ShowRentalSlots.choosing_slot_page))
async def sign_up_to_slot(callback: CallbackQuery, state: FSMContext, db_session):
    callback_data = callback.data.split()
    slot_page = int(callback_data[1])
    slot_number = int(callback_data[2])

    # print(slot_page, slot_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_number = (await state.get_data())['choosing_rental_number']
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)
    date = datetime.today()
    manager = ScheduleManager()
    slots = manager.generate_time_intervals(rentals_schedules, date=date)
    user_id = callback.from_user.id
    slots_per_page = 4
    start_slice = slot_page * slots_per_page
    end_slice = start_slice + slots_per_page
    temporary_slot = slots[start_slice:end_slice][slot_number]
    slot_to_db = SlotCreate(started_at=temporary_slot.start, ended_at=temporary_slot.end, status=SlotStatus.GENERATED,
                            type=SlotType.ACCESSIBLE)
    slot = SlotDAO()
    await slot.create(db_session, slot_to_db)
    # TODO пока затык в создании слота и записи его в базу
    # Создать слот в базе
    # Cоздать рекорд в базе

    await callback.message.edit_text(text=str(f"{temporary_slot.start}\n {type(temporary_slot.start)}"))


@router.callback_query(F.data.startswith('back_to_rentals'), StateFilter(ShowRentalSlots.choosing_slot_page))
async def back_to_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())['choosing_rental_number']
    await state.set_state(ShowRentalSlots.choosing_rental_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedules = await schedule.show_rentals_schedule(db_session, rental_id)
    await callback.message.edit_text(text=display_rental_info(rentals[rental_number], rentals_schedules[0]),
                                     reply_markup=create_rental_pagination_keyboard(rental_number + 1, len(rentals)))


@router.callback_query(F.data == 'to_main_menu')
async def to_main_menu(callback: CallbackQuery, state: FSMContext, db_session):
    await state.clear()
    avalable_rentals: int = 2
    total_rentals: int = 2
    records_amount: int = 0
    await callback.message.edit_text(
        hello_regular_user(callback.from_user.username, avalable_rentals, total_rentals, records_amount),
        reply_markup=create_first_regular_keyboard())

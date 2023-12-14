from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.infra.db.models.rental.dao import RentalDAO
from app.infra.db.models.schedule.dao import ScheduleDAO
from app.telegram.keyboards.regular_user_kb import create_pagination_keyboard

router: Router = Router()


class ShowRental(StatesGroup):
    choosing_rental_number = State()


@router.callback_query(F.data == 'show_rentals', StateFilter(None))
async def show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    await state.set_state(ShowRental.choosing_rental_number)
    rental_number = 0
    await state.update_data(choosing_rental_number=rental_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    await callback.message.edit_text(text=str(rentals[rental_number]),
                                     reply_markup=create_pagination_keyboard(rental_number + 1, len(rentals)))


@router.callback_query(F.data.startswith('shift_show_rentals'), ~StateFilter(None))
async def shift_show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())['choosing_rental_number'] + int(callback.data.split('/')[1])
    await state.update_data(choosing_rental_number=rental_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    await callback.message.edit_text(text=str(rentals[rental_number]),
                                     reply_markup=create_pagination_keyboard(rental_number + 1, len(rentals)))


@router.callback_query(F.data.startswith('schedule '), ~StateFilter(None))
async def show_rentals_schedule(callback: CallbackQuery, state: FSMContext, db_session):
    rental_number = (await state.get_data())['choosing_rental_number']
    # await state.update_data(choosing_rental_number=rental_number)
    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    rental_id = rentals[rental_number].rental_id
    schedule = ScheduleDAO()
    rentals_schedule = await schedule.show_rentals_schedule(db_session, rental_id)

    # await callback.message.edit_text(text=str(rentals[rental_number]),
    #                                  reply_markup=create_pagination_keyboard(rental_number + 1, len(rentals)))
    await callback.bot.send_message(chat_id=callback.message.chat.id, text=str(rentals_schedule))

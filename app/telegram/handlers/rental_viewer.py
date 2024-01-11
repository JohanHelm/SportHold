from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from app.telegram.context.callbacks import RentalsCallbackFactory
from app.telegram.context.querys import RentalQuerys

from app.telegram.context.states import FSMRegularUser

from app.telegram.keyboards.regular_user_kb import (
    create_rental_pagination_keyboard,
    create_first_regular_keyboard,
)

from app.telegram.messages.text_messages import (
    display_rental_info,
    no_rentals_in_db,
)

from app.telegram.utils.db_queries import (
    get_rental_with_suitable_schedules,
    get_rentals_for_user_count,
)

router: Router = Router()


@router.callback_query(F.data == RentalQuerys.SHOW_RENTALS, StateFilter(None))
async def show_rentals(callback: CallbackQuery, state: FSMContext, db_session):
    db_offset = 0
    await state.set_state(FSMRegularUser.choosing_rental_number)
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


@router.callback_query(
    RentalsCallbackFactory.filter(),
    StateFilter(FSMRegularUser.choosing_rental_number),
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

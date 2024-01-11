from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from app.telegram.context.querys import Nav, RentalQuerys
from app.telegram.context.states import FSMRegularUser

from app.telegram.keyboards.regular_user_kb import (
    create_rental_pagination_keyboard,
    create_first_regular_keyboard,
)

from app.telegram.messages.text_messages import (
    display_rental_info,
    hello_regular_user,
)

from app.telegram.utils.db_queries import (
    get_rental_with_suitable_schedules,
    get_rentals_for_user_count,
    get_records_for_user_count,
)

router: Router = Router()


@router.callback_query(
    F.data == RentalQuerys.BACK,
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


@router.callback_query(F.data == Nav.TO_MAIN)
async def to_main_menu(callback: CallbackQuery, state: FSMContext, db_session):
    await state.clear()
    available_rentals: int = await get_rentals_for_user_count(db_session=db_session)
    total_rentals = available_rentals
    records_amount: int = await get_records_for_user_count(
        db_session, callback.from_user.id
    )
    await callback.message.edit_text(
        hello_regular_user(
            callback.from_user.username,
            available_rentals,
            total_rentals,
            records_amount,
        ),
        reply_markup=create_first_regular_keyboard(),
    )

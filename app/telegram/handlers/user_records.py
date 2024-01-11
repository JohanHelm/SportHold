from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.telegram.context.querys import Records
from app.telegram.context.states import FSMRegularUser

from app.telegram.keyboards.regular_user_kb import (
    create_user_records_keyboard,
)

from app.telegram.messages.text_messages import (
    display_user_records,
)

from app.telegram.utils.db_queries import (
    delete_user_record,
    delete_slot_by_id,
    get_rentals_with_user_records,
    get_user_records_to_rental,
)

router: Router = Router()


@router.callback_query(F.data == Records.SHOW_USER_RECORDS, StateFilter(None))
async def show_user_records(callback: CallbackQuery, state: FSMContext, db_session):
    rental_with_record_num = 0
    await state.update_data(rental_with_record=rental_with_record_num)
    rentals_with_user_records = await get_rentals_with_user_records(
        db_session, callback.from_user.id
    )
    if rentals_with_user_records:
        user_records_to_rental = await get_user_records_to_rental(
            db_session,
            callback.from_user.id,
            rentals_with_user_records[rental_with_record_num],
        )
    else:
        user_records_to_rental = ()

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
    F.data.startswith("delete_record"),
    StateFilter(FSMRegularUser.choosing_slot_page, default_state),
)
async def delete_record(callback: CallbackQuery, state: FSMContext, db_session):
    await delete_user_record(db_session, int(callback.data.split("/")[1]))
    # TODO при реализации множественной записи в один слот здесь нужно будет удалять запись из слота
    await delete_slot_by_id(db_session, int(callback.data.split("/")[2]))
    rental_with_record_num = (await state.get_data())["rental_with_record"]
    rentals_with_user_records = await get_rentals_with_user_records(
        db_session, callback.from_user.id
    )
    if rentals_with_user_records:
        user_records_to_rental = await get_user_records_to_rental(
            db_session,
            callback.from_user.id,
            rentals_with_user_records[rental_with_record_num],
        )
    else:
        user_records_to_rental = ()
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
    F.data.startswith("shift_user_records"),
    StateFilter(FSMRegularUser.choosing_slot_page, default_state),
)
async def shift_show_user_records(
    callback: CallbackQuery, state: FSMContext, db_session
):
    rental_with_record_num = (await state.get_data())["rental_with_record"] + int(
        callback.data.split("/")[1]
    )
    await state.update_data(rental_with_record=rental_with_record_num)
    rentals_with_user_records = await get_rentals_with_user_records(
        db_session, callback.from_user.id
    )
    user_records_to_rental = await get_user_records_to_rental(
        db_session,
        callback.from_user.id,
        rentals_with_user_records[rental_with_record_num],
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

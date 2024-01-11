from aiogram import Router, F, types
from aiogram import filters
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from loguru import logger
from sqlalchemy.future import select
from aiogram.enums.chat_type import ChatType
from app.domain.helpers.enums import UserRole, UserStatus
from app.infra.db.models.user.schema import User
from app.telegram.utils.db_queries import (
    add_user,
    get_rentals_for_user_count,
    get_records_for_user_count,
    get_user,
)
from app.telegram.messages.text_messages import (
    help_message,
    hello_regular_user,
    hello_owner_user,
)
from app.telegram.keyboards.regular_user_kb import create_first_regular_keyboard

router: Router = Router()
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.message(CommandStart())
async def process_start_command(message: Message, db_session, state: FSMContext):
    await state.clear()
    user = await get_user(db_session=db_session, user_id=message.from_user.id)
    if not user:
        user = await add_user(
            db_session=db_session,
            user_id=message.from_user.id,
            username=message.from_user.username,
            fullname=message.from_user.full_name,
        )

    if UserRole.REGULAR in UserRole(user.roles):
        available_rentals: int = await get_rentals_for_user_count(db_session=db_session)
        total_rentals = available_rentals
        records_amount: int = await get_records_for_user_count(
            db_session, message.from_user.id
        )
        await message.answer(
            hello_regular_user(
                message.from_user.username,
                available_rentals,
                total_rentals,
                records_amount,
            ),
            reply_markup=create_first_regular_keyboard(),
        )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(help_message)

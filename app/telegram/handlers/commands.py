from aiogram import Router, F
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ChatMemberUpdated
from loguru import logger
from sqlalchemy.future import select

from app.domain.helpers.enums import UserRole, UserStatus
from app.infra.db.models.user.schema import User
from app.telegram.messages.text_messages import help_message, hello_regular_user, hello_owner_user
from app.telegram.keyboards.regular_user_kb import create_first_regular_keyboard

router: Router = Router()
router.my_chat_member.filter(F.chat.type == "private")


@router.message(CommandStart())
async def process_start_command(message: Message, db_session):
    async with db_session() as session:
        result = await session.execute(select(User).where(User.id == message.from_user.id))
        user = result.scalar()
        if not user:
            create_user = User(id=message.from_user.id,
                               username=f"@{message.from_user.username}",
                               fullname=message.from_user.full_name)
            session.add(create_user)
            await session.commit()
            logger.info(f"Bot: We've got new user here. His name: {message.from_user.username},"
                        f" user_id: {message.from_user.id}")
            user = create_user
        await session.refresh(user)
    # TODO логика ветвления в зависимости от роли пользователя
    if UserRole.REGULAR in UserRole(user.roles):
        avalable_rentals: int = 2
        total_rentals: int = 2
        records_amount: int = 0
        await message.answer(
            hello_regular_user(message.from_user.username, avalable_rentals, total_rentals, records_amount),
            reply_markup=create_first_regular_keyboard())
    # elif UserRole.OWNER in user.roles:
    #     await message.answer(hello_owner_user(message.from_user.username), reply_markup=create_first_owner_keyboard())


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(help_message)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, db_session):
    async with db_session() as session:
        result = await session.execute(select(User).where(User.id == event.from_user.id))
        user = result.scalar()
        user.status = UserStatus.INACTIVE.value
        await session.commit()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, db_session):
    async with db_session() as session:
        result = await session.execute(select(User).where(User.id == event.from_user.id))
        user = result.scalar()
        user.status = UserStatus.ACTIVE.value
        await session.commit()

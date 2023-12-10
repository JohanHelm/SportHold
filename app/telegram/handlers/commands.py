from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import Message, ChatMemberUpdated
from loguru import logger

from app.domain.models.user.dto import UserCreate, UserGet
from app.infra.db.models.user.dao import UsedDAO
from app.infra.db.models.rental.dao import RentalDAO
from app.telegram.messages.text_messages import hello_new_user, hello_old_user, help_message
from app.telegram.keyboards.pagintion_kb import create_pagination_keyboard

router: Router = Router()
router.my_chat_member.filter(F.chat.type == "private")


@router.message(CommandStart())
async def process_start_command(message: Message, db_session):
    user_dao = UsedDAO()  # TODO: сделать методы класса статическими
    if not await user_dao.user_exists(db_session, message.from_user.id):
        await user_dao.create(db_session, UserCreate(user_id=message.from_user.id,
                                                     username=f"@{message.from_user.username}",
                                                     fullname=message.from_user.full_name,
                                                     lang_code=message.from_user.language_code,
                                                     registration_date=datetime.now()))
        logger.info(
            f"Bot: We've got new user here. His name: {message.from_user.username}, user_id: {message.from_user.id}")

    # TODO логика ветвления в зависимости от роли пользователя

    rental = RentalDAO()
    rentals = await rental.show_rentals(db_session)
    page = 1
    # for one_rental in rentals:
    #     await message.answer(str(one_rental), reply_markup=create_pagination_keyboard(1, len(rentals)))
    await message.answer(str(rentals[page-1]), reply_markup=create_pagination_keyboard(page, len(rentals)))
    # await message.answer(hello_old_user(message.from_user.username))





@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(help_message)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, db_session):
    user_dao = UsedDAO()
    await user_dao.update_by_user_id(db_session, user_id=event.from_user.id, active=0)
    # TODO разобраться с UserGet, почему для его создания нужны все атрибуты User а не достаточно только user_id


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, db_session):
    user_dao = UsedDAO()
    await user_dao.update_by_user_id(db_session, user_id=event.from_user.id, active=1)

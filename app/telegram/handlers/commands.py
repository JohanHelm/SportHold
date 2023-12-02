from datetime import datetime
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from app.infra.db.models.user.dao import UsedDAO
from app.domain.models.user.dto import UserCreate, UserGet
from app.telegram.messages.text_messages import hello_new_user, hello_old_user, help_message

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, db_session):
    user_dao = UsedDAO()  # TODO: сделать методы класса статическими

    if await user_dao.user_exists(db_session, message.from_user.id):
        await message.answer(hello_old_user(message.from_user.username))
    else:
        await user_dao.create(db_session, UserCreate(user_id=message.from_user.id,
                                                     username=f"@{message.from_user.username}",
                                                     fullname=message.from_user.full_name,
                                                     lang_code=message.from_user.language_code,
                                                     registration_date=datetime.now()))
        logger.info(
            f"Bot: We've got new user here. His name: {message.from_user.username}, user_id: {message.from_user.id}")
        # TODO Написать приветствие нового пользователя
        await message.answer(hello_new_user(message.from_user.username))

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from app.infra.db.models.user.dao import UsedDAO
from app.domain.models.user.dto import UserCreate, UserGet

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, db_session, bot: Bot):
    logger.debug(
        f"Bot: message from: {message.from_user.username}, user_id: {message.from_user.id} message: {message.text}"
    )
    user1 = UserCreate(tg_id=message.from_user.id, username=message.from_user.username)
    user_dao = UsedDAO() # TODO: сделать методы класса статическими
    await user_dao.create(db_session, user1)

    user = await user_dao.get_by_tg_id(db_session, message.from_user.id)
    await message.answer(user.model_dump_json())

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from app.infra.db.models.user.dao import UsedDAO

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, db_session, bot: Bot):
    logger.debug(
        f"get message from: {message.from_user.username}, user_id: {message.from_user.id} message: {message.text}"
    )
    user_dao = UsedDAO() # TODO: сделать методы класса статическими
    user = await user_dao.get_by_id(db_session, id=1)
    await message.answer(user.model_dump_json())

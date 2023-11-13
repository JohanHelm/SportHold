from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.methods import SendMessage
from loguru import logger

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    logger.debug(
        f"get message from: {message.from_user.username}, user_id: {message.from_user.id} message: {message.text}"
    )

    await message.answer("Ola")

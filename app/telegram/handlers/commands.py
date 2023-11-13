from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Ola")

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot, i18n: TranslatorRunner):
    await message.answer(i18n.start())

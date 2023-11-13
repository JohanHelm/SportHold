from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from app.telegram.handlers import commands


async def start_bot(settings):
    logger.debug("Bot online")
    storage = MemoryStorage()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
    )
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(commands.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

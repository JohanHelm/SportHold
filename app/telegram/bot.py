from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from app.telegram.handlers import commands
from app.telegram.middlewares.logging import LoggingMiddleware
from app.telegram.middlewares.db import DbSessionMiddleware
from utils.conf.config import SettingsLoader


async def start_bot():
    settings = SettingsLoader.settings
    logger.debug("Bot online")
    storage = MemoryStorage()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
    )
    dp: Dispatcher = Dispatcher(storage=storage)  # сторейдж заменить на редиску
    dp.include_router(commands.router)  # подумать, как регистрировать сразу все роутеры
    dp.update.middleware(LoggingMiddleware()) # подумать, как регистрировать сразу все сидлвари
    dp.update.middleware(DbSessionMiddleware(uri=settings.DB.URI, echo=True))


    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

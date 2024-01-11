from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from app.telegram.handlers import (
    bot_block_unblock,
    commands,
    regular_user_handlers,
    rental_calendar,
    rental_viewer,
    user_records,
    rental_slots,
)
from app.telegram.middlewares.logging import LoggingMiddleware
from app.telegram.middlewares.db import DbSessionMiddleware
from utils.conf.config import SettingsLoader


async def start_bot():
    settings = SettingsLoader.settings
    logger.debug(f"Configure: bot {settings.BOT_URL}")
    storage = MemoryStorage()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
    )
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(
        commands.router,
        bot_block_unblock.router,
        regular_user_handlers.router,
        rental_viewer.router,
        rental_calendar.router,
        user_records.router,
        rental_slots.router,
    )
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(DbSessionMiddleware(uri=settings.DB.URI, echo=False))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

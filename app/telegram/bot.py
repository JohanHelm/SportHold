from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from app.telegram.handlers import bot_block_unblock, commands, regular_user_handlers
from app.telegram.middlewares.logging import LoggingMiddleware
from app.telegram.middlewares.db import DbSessionMiddleware
from utils.conf.config import SettingsLoader
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def start_bot():
    settings = SettingsLoader.settings
    logger.debug(f"Configure: bot {settings.BOT_URL}")
    storage = MemoryStorage()
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
    )
    dp: Dispatcher = Dispatcher(storage=storage)  # сторейдж заменить на редиску
    dp.include_routers(
        commands.router, bot_block_unblock.router, regular_user_handlers.router
    )  # подумать, как регистрировать сразу все роутеры
    dp.update.middleware(
        LoggingMiddleware()
    )  # подумать, как регистрировать сразу все сидлвари
    dp.update.middleware(DbSessionMiddleware(uri=settings.DB.URI, echo=False))
    scheduler = AsyncIOScheduler()

    try:
        scheduler.start()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()

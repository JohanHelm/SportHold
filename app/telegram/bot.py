import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dynaconf import Dynaconf

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator

from app.utils.conf.config import load_config, get_url
from app.infra.db import create_async_engine_db, async_connection_db
from app.telegram.middlewares import (
    SessionMiddleware,
    RegisteredMiddleware,
)
from app.telegram.handlers import (
    commands,
)

logger = logging.getLogger(__name__)


async def start_bot():
    # -> Logging
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    logger.debug("-> Bot online")

    # -> Config
    config: Dynaconf = load_config("configuration/settings.toml",
                                   "configuration/.secrets.toml", )

    # -> Storage
    storage = MemoryStorage()

    # -> SQLAlchemy
    engine = await create_async_engine_db(url=get_url(config), echo=True)
    db_session = await async_connection_db(engine=engine, expire_on_commit=False)

    # -> Fluentogram
    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en-US",),
        },
        [
            FluentTranslator("ru", translator=FluentBundle.from_files("ru", ["locales/ru.ftl"], )),
            FluentTranslator("en", translator=FluentBundle.from_files("en", ["locales/en.ftl"], ))
        ]
    )

    # -> Bot
    bot: Bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode=config.default_parse_mode,
    )
    dp: Dispatcher = Dispatcher(storage=storage, _translator_hub=translator_hub)

    # -> Middlewares
    dp.update.middleware(SessionMiddleware(session_maker=db_session))
    dp.update.middleware(RegisteredMiddleware())

    # -> Registerer Routers
    dp.include_router(commands.router)

    # -> Start
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               _translator_hub=translator_hub,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

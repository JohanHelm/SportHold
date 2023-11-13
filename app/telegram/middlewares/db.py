from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from loguru import logger
from app.infra.db.pgdb.dal import Builder


class DbSessionMiddleware(BaseMiddleware, Builder):
    def __init__(self, uri, echo):
        super().__init__(uri, echo)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["db_session"] = self.get_session
        return await handler(event, data)

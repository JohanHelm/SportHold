from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from loguru import logger

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug(f"Handler: logging {event.message.from_user.id}") # записывать, от какого пользователя какое сообщение пришло
        result = await handler(event, data) 
        return result
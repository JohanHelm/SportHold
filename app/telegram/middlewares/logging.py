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
        if event.message: # Если пользователь останавливает бота, event.message == None, тогда логгер упадет с ошибкой
            logger.info(
                f"Bot: message from: {event.message.from_user.username},"
                f" user_id: {event.message.from_user.id},"
                f" message: {event.message.text}")
        result = await handler(event, data)
        return result
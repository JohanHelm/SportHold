from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from aiogram.types import Message, CallbackQuery
from loguru import logger

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        event_type = event.event  # Тип апдейта
        if isinstance(event_type, Message):
            logger.info(
                f"Bot: message from: {event.message.from_user.username},"
                f" user_id: {event.message.from_user.id},"
                f" message: {event.message.text}")
        elif isinstance(event_type, CallbackQuery):
            logger.info(
                f"Bot: callback from: {event.callback_query.from_user.username},"
                f" user_id: {event.callback_query.from_user.id},"
                f" callback_data: {event.callback_query.data}")
        result = await handler(event, data)
        return result
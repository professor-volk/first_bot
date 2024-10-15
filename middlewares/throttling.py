from aiogram import BaseMiddleware
from typing import Callable, Dict, Awaitable, Any
from aiogram.types import Message
import logging

class MessageLogMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info(event.text) # Выводим текст сообщения
        return await handler(event, data)
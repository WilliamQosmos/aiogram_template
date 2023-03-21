from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.models.config.main import BotConfig


class SuperUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        config: BotConfig = data['config']
        if event.from_user.id in config.superusers:
            return await handler(event, data)
        else:
            return await event.answer('Вы не суперпользователь')

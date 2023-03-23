from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.models.config.main import Config


class SuperUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        config: Config = data['config']
        if event.from_user.id in config.bot.superusers:
            return await handler(event, data)
        else:
            return await event.answer('Вы не суперпользователь')

from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.dao.holder import HolderDao
from app.models.config import Config
from app.models.db import create_pool


class DBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        config: Config = data.get('config')
        async with create_pool(config.db) as session:
            holder_dao = HolderDao(session)
            data["dao"] = holder_dao
            result = await handler(event, data)
            del data["dao"]
            return result

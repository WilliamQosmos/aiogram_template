from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.dao.holder import HolderDao

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        pool: async_sessionmaker[AsyncSession] = data['db_pool']
        async with pool() as session:
            holder_dao = HolderDao(session)
            data["dao"] = holder_dao
            result = await handler(event, data)
            del data["dao"]
            return result

import asyncio
import logging
import os
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.orm import close_all_sessions

from app.config import load_config
from app.config.logging_config import setup_logging
from app.handlers import setup_handlers
from app.middlewares.data_load_middleware import LoadDataMiddleware
from app.middlewares.db_middleware import DBMiddleware
from app.models.config.main import Paths
from app.models.db import create_pool

logger = logging.getLogger(__name__)


async def main():
    paths = get_paths()

    setup_logging(paths)
    config = load_config(paths)

    if config.bot.storage.is_local:
        storage = MemoryStorage()
    else:
        storage = RedisStorage(config.redis.create_redis)

    dp = Dispatcher(storage=storage, config=config, db_pool=create_pool(config.db))
    dp.message.middleware(DBMiddleware())
    dp.message.middleware(LoadDataMiddleware())
    setup_handlers(dp, config.bot)
    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML",
        session=config.bot.create_session(),
    )
    commands = setup_handlers(dp, config.bot)
    await bot.set_my_commands(commands=commands)

    logger.info("started")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        close_all_sessions()
        logger.info("stopped")


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent)


if __name__ == '__main__':
    asyncio.run(main())

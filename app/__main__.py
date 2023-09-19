import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.orm import close_all_sessions

from app.config import setup_logging
from app.models.config import Config
from app.handlers import setup_handlers
from app.middlewares.data_load_middleware import LoadDataMiddleware
from app.middlewares.db_middleware import DBMiddleware

logger = logging.getLogger(__name__)


async def main():

    setup_logging()
    config = Config()

    if config.bot.storage.is_local:
        storage = MemoryStorage()
    else:
        storage = RedisStorage(config.create_redis)

    dp = Dispatcher(storage=storage, config=config, db_pool=config.create_db_pool)
    dp.message.middleware(DBMiddleware())
    dp.message.middleware(LoadDataMiddleware())
    bot = Bot(
        token=config.TG_BOT_TOKEN,
        parse_mode="HTML",
        session=config.create_bot_session(),
    )
    commands = setup_handlers(dp, config)
    await bot.set_my_commands(commands=commands)

    logger.info("started")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        close_all_sessions()
        logger.info("stopped")


if __name__ == '__main__':
    asyncio.run(main())

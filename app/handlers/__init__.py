import logging

from aiogram import Dispatcher

from app.handlers.base import router as base
from app.handlers.errors import setup_errors
from app.handlers.superuser import router as superuser
from app.models.config.main import BotConfig

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    setup_errors(dp, bot_config.log_chat)
    dp.include_router(base)
    dp.include_router(superuser)
    logger.debug("handlers configured successfully")

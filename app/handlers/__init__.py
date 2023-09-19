import logging
from typing import Generator, Tuple

from aiogram import Dispatcher, Router
from aiogram.filters import Command

from app.handlers.base import router as base
from app.handlers.errors import setup_errors
from app.handlers.superuser import router as superuser
from app.models.config import Config

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, config: Config):
    setup_errors(dp, config.LOGGING_CHAT_ID)
    dp.include_router(base)
    dp.include_router(superuser)
    base_commands = collect_commands(base)
    superuser_commands = collect_commands(superuser)
    commands = [*base_commands, *superuser_commands]
    logger.debug(commands)
    logger.debug("handlers configured successfully")
    return commands


def collect_commands(router: Router) -> Generator[Tuple[Command, str], None, None]:
    for handler in router.message.handlers:
        if "commands" not in handler.flags:
            continue
        for command in handler.flags["commands"]:
            yield {"command": command.commands[0], "description": handler.callback.__doc__ or "No description available"}
    for sub_router in router.sub_routers:
        yield from collect_commands(sub_router)

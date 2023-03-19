from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from functools import partial

from app.filters.superusers import SuperUserFilter
from app.models.config.main import BotConfig

router = Router(name=__name__)

async def exception(message: Message):
    raise RuntimeError(message.text)


async def leave_chat(message: Message, bot: Bot):
    await bot.leave_chat(message.chat.id)


def setup_superuser(dp: Dispatcher, bot_config: BotConfig):
    router.message.filter(SuperUserFilter(bot_config.superusers))
    router.message.register(exception, Command(commands="exception"))
    router.message.register(leave_chat, Command(commands="get_out"))

    dp.include_router(router)

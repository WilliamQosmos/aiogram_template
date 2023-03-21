from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.middlewares.superuser_middleware import SuperUserMiddleware

router = Router(name=__name__)
router.message.middleware(SuperUserMiddleware())

@router.message(Command(commands="exception"))
async def exception(message: Message):
    raise RuntimeError(message.text)


@router.message(Command(commands="get_out"))
async def leave_chat(message: Message, bot: Bot):
    await bot.leave_chat(message.chat.id)

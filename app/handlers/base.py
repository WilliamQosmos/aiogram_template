import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentType

from aiogram.utils.markdown import html_decoration as hd

from app.dao.holder import HolderDao
from app.models import dto
from app.services.chat import update_chat_id

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(Command("start"))
async def start_cmd(message: Message):
    """Start"""
    await message.reply("Hi!")


@router.message(Command(commands=["idchat", "chat_id", "id"], prefix="/!"))
async def chat_id(message: Message):
    """Get chat id"""
    text = (
        f"chat_id: {hd.pre(message.chat.id)}\n"
        f"your user_id: {hd.pre(message.from_user.id)}"
    )
    if message.reply_to_message:
        text += (
            f"\nid {hd.bold(message.reply_to_message.from_user.full_name)}: "
            f"{hd.pre(message.reply_to_message.from_user.id)}"
        )
    await message.reply(text, disable_notification=True)


@router.message(Command(commands="cancel"))
async def cancel_state(message: Message, state: FSMContext):
    """Cancel all state"""
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info('Cancelling state %s', current_state)
    await state.clear()
    await message.reply('Dialog stopped, data removed', reply_markup=ReplyKeyboardRemove())


@router.message(F.content_types == ContentType.MIGRATE_TO_CHAT_ID)
async def chat_migrate(message: Message, chat: dto.Chat, dao: HolderDao):
    new_id = message.migrate_to_chat_id
    await update_chat_id(chat, new_id, dao.chat)
    logger.info("Migrate chat from %s to %s", message.chat.id, new_id)

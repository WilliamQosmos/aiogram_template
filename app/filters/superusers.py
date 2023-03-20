from aiogram.types import Message

from aiogram.filters import BaseFilter

from app.models.config.main import BotConfig


class SuperUserFilter(BaseFilter):
    def __init__(self, config: BotConfig):  # [2]
        self.superusers = config.superusers

    async def __call__(self, message: Message) -> bool:  # [3]
        return message.from_user.id in self.superusers

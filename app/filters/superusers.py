from aiogram.types import Message

from aiogram.filters import BaseFilter

class SuperUserFilter(BaseFilter):
    def __init__(self, superusers: list[int]):  # [2]
        self.superusers = superusers

    async def __call__(self, message: Message) -> bool:  # [3]
        return message.from_user.id in self.superusers

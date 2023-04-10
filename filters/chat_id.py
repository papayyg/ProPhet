from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class ChatIDFilter(BoundFilter):
    key = "chat_id"

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    async def check(self, message: Message):
        return message.chat.id == self.chat_id
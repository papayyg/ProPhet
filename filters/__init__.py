from aiogram import Dispatcher

from .chat_id import ChatIDFilter
from .chat_type import ChatTypeFilter
from .is_admin import IsAdminFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdminFilter)
    dp.filters_factory.bind(ChatTypeFilter)
    dp.filters_factory.bind(ChatIDFilter)

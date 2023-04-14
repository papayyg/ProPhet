import asyncio
from random import choice

import aioschedule
from aiogram import Dispatcher

from data.config import log_channel
from utils.db.aiomysql import BotDB

locales_dict = {}

async def get_chats_locales():
    result = await BotDB.get_local()
    global locales_dict
    for tup in result:
        locales_dict[int(tup[0])] = tup[1]
    


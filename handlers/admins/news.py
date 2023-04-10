from aiogram import types

from data.config import owner_id
from loader import dp
from utils.db.aiomysql import BotDB


@dp.message_handler(commands=['news'], commands_prefix="/!@", user_id=owner_id)
async def command_ping(message: types.Message):
    chats = await BotDB.all_chats()
    for chat in chats:
        try:
            await dp.bot.send_message(chat[0], message.text[6:])
            print(f'Отправил {chat[0]}')
        except:
            continue
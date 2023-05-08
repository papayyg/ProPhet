from aiogram import types

from data.config import owner_id
from loader import dp
from utils.db.aiomysql import BotDB

from utils.locales import locales_dict

@dp.message_handler(commands=['news'], commands_prefix="/!@", user_id=owner_id)
async def command_ping(message: types.Message):
    text = message.text[6:].split('AZ')
    text_ru = text[0]
    text_az = text[1]
    chats = await BotDB.all_chats()
    for chat in chats:
        chat_id = int(chat[0])
        if chat_id > 0:
            try:
                if locales_dict[chat_id] == 'ru':
                    await dp.bot.send_message(chat_id, text_ru)
                else:
                    await dp.bot.send_message(chat_id, text_az)
                print(f'Отправил {chat[0]}')
            except:
                continue
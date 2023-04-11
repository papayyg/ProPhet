from aiogram import types

from data.config import log_channel
from loader import dp
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit


@rate_limit(limit=10)
@dp.message_handler(commands=['start'], commands_prefix="/!@")
async def start_command(message: types.Message):
    await message.answer('<b>Приветствую тебя, мой друг!</b> Я бот, созданный для того, чтобы <i>облегчить твою жизнь и '
                         'сделать ее более продуктивной</i>. \n\nС моими возможностями ты можешь ознакомиться '
                         'использовав'
                         ' команду - /help')
    if await BotDB.chats_exists(message.chat.id):
        await BotDB.chat_update(message.chat.id, message.from_user.first_name)
    else:
        await BotDB.add_chat(message.chat.id, message.from_user.first_name)
        await dp.bot.send_message(log_channel, f'🟣 {message.from_user.get_mention(as_html=True)} подписался на бота!')
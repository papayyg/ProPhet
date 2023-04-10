from aiogram import types
from aiogram.dispatcher.filters import Regexp

from loader import dp
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit


@rate_limit(limit=5)
@dp.message_handler(chat_type=["group", "supergroup"], commands=['in'], commands_prefix="/!@")
async def command_in(message: types.Message):
    if await BotDB.check_chat_user(message.chat.id, message.from_user.id) == 0:
        await BotDB.add_user(message.chat.id, message.from_user.id,
                       message.from_user.first_name, message.from_user.username)
        await message.answer(f'{message.from_user.first_name} добавлен в список')
    else:
        await message.answer('Вы уже в списке')

@rate_limit(limit=5)
@dp.message_handler(chat_type=["group", "supergroup"], commands=['out'], commands_prefix="/!@")
async def send_welcome(message: types.Message):
    if message.chat.id == -1001299519078:
        await message.reply('Бездарям запрещена команда')
        return
    if await BotDB.check_chat_user(message.chat.id, message.from_user.id):
        await BotDB.remove_user(message.chat.id, message.from_user.id)
        await message.answer(f'{message.from_user.first_name} удалён из списка')
    else:
        await message.answer('Вас нет в списке')

@rate_limit(limit=10)
@dp.message_handler(Regexp("(@|/|!)all"), chat_type=["group", "supergroup"])
async def all_command(message: types.Message):
    if await BotDB.check_chat(message.chat.id):
        p = ''
        for line in await BotDB.all_user(message.chat.id):
            p += f'<a href="tg://user?id={line[0]}">{line[1]}</a> '
        if message.reply_to_message: await dp.bot.send_message(message.chat.id, p, reply_to_message_id=message.reply_to_message.message_id)
        else: await message.reply(p)
    else:
        await message.reply('Сперва используйте /in')
import re
from random import choice, randint

from aiogram import types

from loader import dp
from service import basic
from utils.misc.throttling import rate_limit


@rate_limit(limit=1)
@dp.message_handler(commands=['n'], commands_prefix="/!@", is_reply=False)
async def command_n(message: types.Message):
    await message.reply(choice(['Да', 'Нет']))

@dp.message_handler(commands=['n'], commands_prefix="/!@", is_reply=True)
async def command_n(message: types.Message):
    await dp.bot.send_message(chat_id=message.chat.id, text=choice(['Да', 'Нет']),
                              reply_to_message_id=message.reply_to_message.message_id)

@rate_limit(limit=1)
@dp.message_handler(commands=['l'], commands_prefix="/!@", is_reply=False)
async def command_l(message: types.Message):
    matches = re.findall(r"\d+", message.text)
    if len(matches) != 2:
        await message.reply('Введите через пробел два значения')
    else:
        try:
            random_number = await basic.random_l(matches)
            await message.reply(random_number)
        except ValueError:
            await message.reply('Неправильное значение')

@dp.message_handler(commands=['l'], commands_prefix="/!@", is_reply=True)
async def command_l(message: types.Message):
    matches = re.findall(r"\d+", message.reply_to_message.text)
    if len(matches) != 2:
        await message.reply('Введите через пробел два значения')
    else:
        try:
            random_number = await basic.random_l(matches)
            await dp.bot.send_message(chat_id=message.chat.id, text=random_number,
                                      reply_to_message_id=message.reply_to_message.message_id)
        except ValueError:
            await message.reply('Неправильное значение')

@rate_limit(limit=1)
@dp.message_handler(commands=['k'], commands_prefix="/!@")
async def command_k(message: types.Message):
    text = message.reply_to_message.text if message.reply_to_message else message.text.split(' ', 1)[-1]
    if ' ' in text:
        words = text.split()
        try:
            await (message.reply_to_message or message).reply(choice(words))
        except:
            await message.reply('Неправильное значение')
    else:
        await message.reply('Введите несколько значений через пробел')

@rate_limit(limit=1)
@dp.message_handler(commands=['coin'], commands_prefix="/!@")
async def command_coin(message: types.Message):
    await message.reply(choice(['Орёл', 'Решка']))

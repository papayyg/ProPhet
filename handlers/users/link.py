import pyshorteners
from aiogram import types

from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(limit=4)
@dp.message_handler(commands=['link'], commands_prefix="/!@", is_reply=True, content_types=types.ContentTypes.TEXT)
async def shorter_link_reply(message: types.Message):
    text = message.reply_to_message.text
    if ' ' not in text and text.startswith('http'):
        try:
            url = message.reply_to_message.text
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(url)
        except:
            short_url = 'Некорректная ссылка'
        await dp.bot.send_message(message.chat.id, short_url, reply_to_message_id=message.reply_to_message.message_id)
    else:
        await message.reply('Некорректная ссылка')

@rate_limit(limit=4)
@dp.message_handler(commands=['link'], commands_prefix="/!@")
async def shorter_link(message: types.Message):
    text = message.text
    if text.find(' ') != -1:
        try:
            url = message.text[text.find(' ') + 1:]
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(url)
        except:
            short_url = 'Некорректная ссылка'
        await message.reply(short_url)
    else:
        await message.answer('Отправьте ссылку через пробел после команды или ответом на ссылку')
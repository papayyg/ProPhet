from aiogram import types
from googletrans import Translator

from loader import dp

translator = Translator()

@dp.message_handler(commands=['translate'], commands_prefix="/!@")
async def translate(message: types.Message):
    try:
        text = message.reply_to_message.text if message.reply_to_message else message.text.split(' ', 1)[1]
    except:
        await message.reply('Введите текст для перевода')
        return
    dest = 'en' if translator.detect(text).lang == 'ru' else 'ru'
    if message.reply_to_message:
        await dp.bot.send_message(chat_id=message.chat.id, text=translator.translate(text, dest=dest).text, reply_to_message_id=message.reply_to_message.message_id)
    else:
        await message.reply(translator.translate(text, dest=dest).text)

@dp.message_handler(commands=['translateto'], commands_prefix="/!@")
async def translate_to(message: types.Message):
    try:
        text = message.reply_to_message.text if message.reply_to_message else message.text[message.text.find(' ', message.text.find(' ') + 1) + 1:]
        dest = message.text[message.text.find(' ') + 1:] if message.reply_to_message else message.text[message.text.find(' ') + 1:message.text.find(' ', message.text.find(' ') + 1)]
        translation = translator.translate(text, dest=dest).text
        if message.reply_to_message:
            await dp.bot.send_message(chat_id=message.chat.id, text=f'{translation}',
                                   reply_to_message_id=message.reply_to_message.message_id)
        else:
            await message.reply(f'{translation}')
    except Exception as ex:
        await message.reply(f'⚠️ Ошибка: {translator.translate(ex, dest="ru").text}')

from random import choice

from aiogram import types

from loader import dp

from locales.translations import _
from utils.locales import locales_dict

from utils.logs import send_logs

async def answers(lang):
    answer = ['Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да',
          'Можешь быть уверен в этом', 'Мне кажется - да', 'Вероятнее всего',
          'Хорошие перспективы', 'Знаки говорят - да', 'Да', 'Пока неясно, попробуй снова',
          'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать',
          'Сконцентрируйся и спроси опять', 'Даже не думай', 'Мой ответ - нет',
          'По моим данным - нет', 'Перспективы не очень хорошие', 'Весьма сомнительно']
    return await _(choice(answer), locales_dict[lang])

@dp.message_handler(lambda message: message.text.lower() == 'шар' or message.text.lower() == 'kürə', is_reply=False)
async def shar(message: types.Message):
    await message.reply('Да, мой Господин?')

@dp.message_handler(lambda message: message.text.lower() == 'шар' or message.text.lower() == 'kürə', is_reply=True)
async def shar(message: types.Message):
    await dp.bot.send_message(message.chat.id, await answers(message.chat.id), reply_to_message_id=message.reply_to_message.message_id)
    await send_logs(message.from_user.first_name, message.text)

@dp.message_handler(lambda message: message.text.lower().startswith('шар,') or message.text.lower().startswith('kürə,'))
async def shar(message: types.Message):
    await message.reply(await answers(message.chat.id))
    await send_logs(message.from_user.first_name, message.text)
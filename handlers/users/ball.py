from random import choice

from aiogram import types

from loader import dp

answer = ['Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да',
          'Можешь быть уверен в этом', 'Мне кажется - да', 'Вероятнее всего',
          'Хорошие перспективы', 'Знаки говорят - да', 'Да', 'Пока неясно, попробуй снова',
          'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать',
          'Сконцентрируйся и спроси опять', 'Даже не думай', 'Мой ответ - нет',
          'По моим данным - нет', 'Перспективы не очень хорошие', 'Весьма сомнительно']

@dp.message_handler(lambda message: message.text.lower() == 'шар', is_reply=False)
async def shar(message: types.Message):
    await message.reply('Да, мой Господин?')

@dp.message_handler(lambda message: message.text.lower() == 'шар', is_reply=True)
async def shar(message: types.Message):
    await dp.bot.send_message(message.chat.id, choice(answer), reply_to_message_id=message.reply_to_message.message_id)

@dp.message_handler(lambda message: message.text.lower().startswith('шар,'))
async def shar(message: types.Message):
    await message.reply(choice(answer))
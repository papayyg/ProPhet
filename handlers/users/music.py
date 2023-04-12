from aiogram import types

from loader import bot, dp

data = {
    'ууу': {
        "src": "Serega",
        "performer": 'Serega',
        "title": 'Where is my mind',
    },
    'гост': {
        "src": "Ghostly",
        "performer": 'Viral Sound God',
        "title": 'Ghostly',
    },
    'хоко': {
        "src": "Grustno",
        "performer": 'Eslabon Armado',
        "title": 'Jugaste y Sufri',
    },
    'уэнсдей': {
        "src": "Wednesday",
        "performer": 'Лизогуб',
        "title": 'ДЕВОЧКА УЭНСДЕЙ',
    },
    'густас': {
        "src": "Gustas",
        "performer": 'Manu Chao',
        "title": 'Me Gustas Tu',
    },
}

@dp.message_handler(lambda message: message.text.lower() in ['ууу', 'гост', 'хоко', 'уэнсдей', 'густас'])
async def send_music(message: types.Message):
    audio = open(f'data/music/{data[message.text.lower()]["src"]}.mp3', 'rb')
    if message.reply_to_message:
        await bot.send_audio(message.chat.id, audio, title=data[message.text]["title"], performer=data[message.text]["performer"], reply_to_message_id=message.reply_to_message.message_id)
    else:
        await bot.send_audio(message.chat.id, audio, title=data[message.text]["title"], performer=data[message.text]["performer"])
    await bot.delete_message(message.chat.id, message.message_id)
    audio.close()
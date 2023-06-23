from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from aiogram.types import InputFile
from service import apple


@rate_limit(limit=5)
@dp.message_handler(lambda message: (message.text.startswith('https://music.apple.com/') and 'playlist' not in message.text))
async def spotify_download(message: types.Message):
    path = message.from_user.id - message.message_id
    url = message.text

    user = message.from_user.get_mention(as_html=True)
    if message.chat.title:
        caption = f"👤 {user} - 🎶 <i>*<a href='{message.text}'>Музыка</a>*</i>"
    else:
        caption = f"🎶 <i><a href='{message.text}'>Музыка</a></i>"

    if await apple.get_music(url, path):
        music = InputFile(f'temp/apple_{path}.mp3')
        image = InputFile(f'temp/image_{path}.jpg')
        await message.answer_audio(music, caption=caption, thumb=image)
        await message.delete()
        remove(f'temp/apple_{path}.mp3')
        remove(f'temp/image_{path}.jpg')
    else:
        await message.answer('Ошибка. Повторите попытку')
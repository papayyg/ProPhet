from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from yandex_music import ClientAsync
from aiogram.types import InputFile
import re
from data.config import YANDEX_TOKEN


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://music.yandex.ru/album/') and 'track' in message.text)
async def yandex_download(message: types.Message):
    client = await ClientAsync(YANDEX_TOKEN).init()
    url = message.text
    album_id = re.search(r"/album/(\d+)/", url).group(1)
    track_id = re.search(r"/track/(\d+)$", url).group(1)
    result = f"{track_id}:{album_id}"
    short_track = (await client.tracks([result]))[0]
    title, artist = short_track['title'], short_track['artists'][0]['name']
    await short_track.download_async(f'temp/{message.from_user.id - message.message_id}.mp3')
    music = InputFile(f'temp/{message.from_user.id - message.message_id}.mp3')
    user = message.from_user.get_mention(as_html=True)
    if message.chat.title:
        caption = f"👤 {user} - 🎶 <i>*<a href='{message.text}'>Музыка</a>*</i>"
    else:
        caption = f"🎶 <i><a href='{message.text}'>Музыка</a></i>"
    await message.answer_audio(music, title=title, performer=artist, caption=caption)
    await message.delete()
    remove(f'temp/{message.from_user.id - message.message_id}.mp3')
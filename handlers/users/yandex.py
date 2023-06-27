from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from yandex_music import ClientAsync, Cover
from aiogram.types import InputFile
import re
from data.config import YANDEX_TOKEN
import requests
from bs4 import BeautifulSoup
from utils.logs import send_logs



@rate_limit(limit=5)
@dp.message_handler(lambda message: (message.text.startswith('https://music.yandex.ru/album/') or message.text.startswith('https://music.yandex.com/album/')) and 'track' in message.text)
async def yandex_download(message: types.Message):
    client = await ClientAsync(YANDEX_TOKEN).init()
    url = message.text
    album_id = re.search(r"/album/(\d+)/", url).group(1)
    track_id = re.search(r"/track/(\d+)$", url).group(1)
    result = f"{track_id}:{album_id}"
    short_track = (await client.tracks([result]))[0]
    await short_track.download_cover_async(f'temp/image_{message.from_user.id - message.message_id}.jpg')
    title, artist = short_track['title'], short_track['artists'][0]['name']
    await short_track.download_async(f'temp/{message.from_user.id - message.message_id}.mp3')
    music = InputFile(f'temp/{message.from_user.id - message.message_id}.mp3')
    img = InputFile(f'temp/image_{message.from_user.id - message.message_id}.jpg')
    user = message.from_user.get_mention(as_html=True)
    if message.chat.title:
        caption = f"👤 {user} - 🎶 <i>*<a href='{message.text}'>Музыка</a>*</i>"
    else:
        caption = f"🎶 <i><a href='{message.text}'>Музыка</a></i>"
    await message.answer_audio(music, title=title, performer=artist, caption=caption, thumb=img)
    await message.delete()
    remove(f'temp/{message.from_user.id - message.message_id}.mp3')
    remove(f'temp/image_{message.from_user.id - message.message_id}.jpg')
    await send_logs(message.from_user.first_name, message.text)
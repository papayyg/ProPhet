from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from aiogram.types import InputFile
from service import spotify
from data.config import YANDEX_TOKEN
from yandex_music import ClientAsync


async def get_yandex(music_search, path, track_title):
    client = await ClientAsync(YANDEX_TOKEN).init()
    result = (await client.search(music_search)).best
    track_id, album_id = result["result"]["id"], result["result"]["albums"][0]["id"]
    music_id = f'{track_id}:{album_id}'
    short_track = (await client.tracks([music_id]))[0]
    title = short_track['title']
    if title != track_title:
        raise ValueError("Ошибка: несоответствие имен")
    await short_track.download_async(f'temp/audio_{path}.mp3')


@rate_limit(limit=5)
@dp.message_handler(lambda message: (message.text.startswith('https://open.spotify.com/track/')))
async def spotify_download(message: types.Message):
    track_id = message.text.split("/")[4].split("?")[0]
    path = message.from_user.id - message.message_id
    track_info = await spotify.get_spotify_track_info(await spotify.get_spotify_access_token(), track_id)
    await spotify.download_cover_image(track_info["album"]["images"][0]["url"], path)

    track_title = track_info["name"]
    artists = track_info["artists"][0]["name"]
    image = InputFile(f'temp/image_{path}.jpg')

    user = message.from_user.get_mention(as_html=True)
    if message.chat.title:
        caption = f"👤 {user} - 🎶 <i>*<a href='{message.text}'>Музыка</a>*</i>"
    else:
        caption = f"🎶 <i><a href='{message.text}'>Музыка</a></i>"

    music_search = f'{track_info["artists"][0]["name"]} - {track_info["name"]}'

    try:
        await get_yandex(music_search, path, track_title)
    except:
        try:
            video_id = await spotify.search_youtube_video(music_search)
            await spotify.download_audio(video_id, path)
        except:
            await message.answer('Ошибка. Повторите попытку.')
            return
    
    music = InputFile(f'temp/audio_{path}.mp3')
    await message.answer_audio(music, title=track_title, performer=artists, caption=caption, thumb=image)
    await message.delete()
    remove(f'temp/audio_{path}.mp3')
    remove(f'temp/image_{path}.jpg')
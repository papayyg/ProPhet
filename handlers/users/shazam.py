from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from yandex_music import ClientAsync
from aiogram.types import InputFile
import re
from shazamio import Shazam
from data.config import YANDEX_TOKEN, CLIENT_ID, CLIENT_SECRET
import httpx
import asyncio
from service import spotify
from utils.logs import send_logs


async def get_spotify_link(title, author):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    async with httpx.AsyncClient() as client:
        auth_response = await client.post(AUTH_URL, data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        endpoint = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {auth_response.json()["access_token"]}'}
        params = {
            'q': f"{title} {author}", 'type': 'track', 'limit': 1}
        response = await client.get(endpoint, headers=headers, params=params)
        return response.json()["tracks"]["items"][0]["external_urls"]["spotify"]
    


async def get_spotify(link, path):
    track_id = link.split("/")[4].split("?")[0]
    track_info = await spotify.get_spotify_track_info(await spotify.get_spotify_access_token(), track_id)
    await spotify.download_cover_image(track_info["album"]["images"][0]["url"], path)
    track_title = track_info["name"]
    artists = track_info["artists"][0]["name"]
    image = InputFile(f'temp/image_{path}.jpg')
    music_search = f'{track_info["artists"][0]["name"]} - {track_info["name"]}'
    video_id = await spotify.search_youtube_video(music_search)
    await spotify.download_audio(video_id, path)
    return track_title, artists, image


async def get_yandex(message, title, author):
    client = await ClientAsync(YANDEX_TOKEN).init()
    result = (await client.search(f"{title} {author}")).best
    track_id, album_id = result["result"]["id"], result["result"]["albums"][0]["id"]
    music_id = f'{track_id}:{album_id}'
    short_track = (await client.tracks([music_id]))[0]
    new_title, artist = short_track['title'], short_track['artists'][0]['name']
    await short_track.download_cover_async(f'temp/image_{message.from_user.id - message.message_id}.jpg')
    await short_track.download_async(f'temp/yandex_{message.from_user.id - message.message_id}.mp3')
    return new_title, artist, f'https://music.yandex.ru/album/{album_id}/track/{track_id}'


@rate_limit(limit=3)
@dp.message_handler(commands=['shazam'], commands_prefix="/!@")
async def shazam_command(message: types.Message):
    temp = await message.reply('Ожидайте...')
    shazam = Shazam()
    if message.reply_to_message:
        if message.reply_to_message.audio:
            file = await dp.bot.get_file(message.reply_to_message.audio.file_id)
        elif message.reply_to_message.voice:
            file = await dp.bot.get_file(message.reply_to_message.voice.file_id)
        elif message.reply_to_message.video_note:
            file = await dp.bot.get_file(message.reply_to_message.video_note.file_id)
        elif message.reply_to_message.video:
            file = await dp.bot.get_file(message.reply_to_message.video.file_id)
        else:
            await temp.edit_text('Введите ответом на аудио/видео/голосовое сообщение/видеосообщение')
            return
        await dp.bot.download_file(file.file_path, f"temp/{message.from_user.id - message.message_id}.mp3")
        out = await shazam.recognize_song(f"temp/{message.from_user.id - message.message_id}.mp3")
        if len(out['matches']) == 0:
            await temp.edit_text('К сожалению, я не могу определить что за песня.')
            return
        user = message.from_user.get_mention(as_html=True)
        if message.chat.title:
            caption = f"👤 {user}\n\n🎶 <b><i>{out['track']['title']} - {out['track']['subtitle']}</i></b>"
        else:
            caption = f"🎶 <b><i>{out['track']['title']} - {out['track']['subtitle']}</i></b>"
        await temp.delete()
        temp = await bot.send_photo(message.chat.id, out["track"]["images"]["coverart"], caption, reply_to_message_id=message.reply_to_message.message_id)
        remove(f'temp/{message.from_user.id - message.message_id}.mp3')
        try:
            title, artist, yandex_link = await get_yandex(message, out['track']['title'], out['track']['subtitle'])
            spotify_link = await get_spotify_link(out['track']['title'], out['track']['subtitle'])
            music = InputFile(f'temp/yandex_{message.from_user.id - message.message_id}.mp3')
            img = InputFile(f'temp/image_{message.from_user.id - message.message_id}.jpg')
            await bot.send_audio(message.chat.id, music, f'🎧 <b><i><a href="{yandex_link}">Яндекс.Музыка</a>\n🎶 <a href="{spotify_link}">Spotify</a></i></b>', reply_to_message_id=temp.message_id, title=title, performer=artist, thumb=img)
            remove(f"temp/yandex_{message.from_user.id-message.message_id}.mp3")
            remove(f'temp/image_{message.from_user.id - message.message_id}.jpg')
        except:
            spotify_link = await get_spotify_link(out['track']['title'], out['track']['subtitle'])
            track_title, artists, image = await get_spotify(spotify_link, message.from_user.id - message.message_id)
            music = InputFile(f'temp/audio_{message.from_user.id - message.message_id}.mp3')
            await bot.send_audio(message.chat.id, music, f'🎧 <b><i><a href="{spotify_link}">Spotify</a></i></b>', reply_to_message_id=temp.message_id, title=track_title, performer=artists, thumb=image)
            remove(f"temp/audio_{message.from_user.id-message.message_id}.mp3")
            remove(f"temp/image_{message.from_user.id-message.message_id}.jpg")
    else:
        await temp.edit_text('Введите ответом на аудио/видео/голосовое сообщение/видеосообщение')
    await send_logs(message.from_user.first_name, message.text)

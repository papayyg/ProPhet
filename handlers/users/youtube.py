import asyncio
from functools import partial
from os import remove

from aiogram import types
from pytube import YouTube

from loader import bot, dp
from utils.misc.throttling import rate_limit
from aiogram.types import InputFile

import aiohttp
import isodate
from data.config import YOUTUBE_API
import re

from service import youtube
from keyboards import inline_kp_youtube


headers = {
    'Accept': 'application/json',
}


async def info_video(url):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\&|\?)?", r"youtu\.be\/([0-9A-Za-z_-]{11})"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&part=contentDetails&id={video_id}&key={YOUTUBE_API}') as response:
            json_data = (await response.json())["items"][0]
            title = json_data["snippet"]["title"]
            author = json_data["snippet"]["channelTitle"]
            duration = isodate.parse_duration(
            json_data["contentDetails"]["duration"]).total_seconds()
            return duration, author, title


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtube.com/watch?v=') or message.text.startswith('https://youtu.be/') or message.text.startswith('https://www.youtube.com/shorts/') or message.text.startswith('https://youtube.com/shorts/'), chat_type=["group", "supergroup"])
async def videos_group(message: types.Message):
    # try:
        duration, author, title = await info_video(message.text)
        if int(duration) < 600:
            await youtube.download_video(message.text, message.from_user.id - message.message_id)
            video = InputFile(
                f'temp/youtube_video_{message.from_user.id - message.message_id}.mp4')
            caption = f'👤 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            await bot.send_video(chat_id=message.chat.id, video=video,
                                caption=caption)
            await bot.delete_message(message.chat.id, message.message_id)
            remove(
                f'temp/youtube_video_{message.from_user.id - message.message_id}.mp4')
    # except Exception as ex:
    #     print(ex)
    #     await message.answer('Ошибка. Повторите попытку (Возможно видео недоступно).')


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtube.com/watch?v=') or message.text.startswith('https://youtu.be/') or message.text.startswith('https://www.youtube.com/shorts/') or message.text.startswith('https://youtube.com/shorts/'))
async def videos_private(message: types.Message):
    # try:
        duration, author, title = await info_video(message.text)
        if int(duration) < 600:
            yt_kb = await inline_kp_youtube.youtube_kb(f'{message.text}', message.chat.id)
            await message.reply(f'<b>Выберите формат для загрузки:</b>\n<i>{author}\n{title}</i>', reply_markup=yt_kb)
    # except Exception as ex:
    #     print(ex)
    #     await message.answer('Ошибка. Повторите попытку (Возможно видео недоступно).')


@dp.callback_query_handler(lambda c: c.data.startswith('yt_video:'))
async def youtube_video_kb(callback: types.CallbackQuery):
    temp = await bot.edit_message_text('Ожидайте...', chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    data = callback.message.text.split('\n')
    url = ":".join(callback.data.split(':')[1:])
    author = data[1]
    title = data[2]
    await youtube.download_video(url, callback.message.from_user.id - callback.message.message_id)
    video = InputFile(
        f'temp/youtube_video_{callback.message.from_user.id - callback.message.message_id}.mp4')
    caption = f'👤 <a href="{callback.message.reply_to_message.text}">{author}</a>\n\n📝 {title}'
    await bot.send_video(chat_id=callback.message.chat.id, video=video,
                         caption=caption)
    await bot.delete_message(callback.message.chat.id, callback.message.reply_to_message.message_id)
    await temp.delete()
    remove(
        f'temp/youtube_video_{callback.message.from_user.id - callback.message.message_id}.mp4')


@dp.callback_query_handler(lambda c: c.data.startswith('yt_audio:'))
async def youtube_audio_kb(callback: types.CallbackQuery):
    temp = await bot.edit_message_text('Ожидайте...', chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    data = callback.message.text.split('\n')
    url = ":".join(callback.data.split(':')[1:])
    author = data[1]
    title = data[2]
    await youtube.download_audio(url, callback.message.from_user.id - callback.message.message_id)
    audio = InputFile(
        f'temp/youtube_audio_{callback.message.from_user.id - callback.message.message_id}.mp3')
    caption = f'👤 <a href="{callback.message.reply_to_message.text}">{author}</a>\n\n📝 {title}'
    await bot.send_audio(chat_id=callback.message.chat.id, audio=audio, title=title, performer=author, caption=caption)
    await bot.delete_message(callback.message.chat.id, callback.message.reply_to_message.message_id)
    await temp.delete()
    remove(
        f'temp/youtube_audio_{callback.message.from_user.id - callback.message.message_id}.mp3')

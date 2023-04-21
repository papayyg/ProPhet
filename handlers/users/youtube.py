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


headers = {
    'Accept': 'application/json',
}


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/shorts/') or message.text.startswith('https://youtube.com/shorts/'))
async def shorts(message: types.Message):
    try:
        video_url = message.text
        loop = asyncio.get_event_loop()
        yt = await loop.run_in_executor(None, partial(YouTube, video_url))
        author = yt.author
        title = yt.title
        stream = yt.streams.get_highest_resolution()
        await loop.run_in_executor(None, partial(stream.download, filename=f'temp/{str(message.from_user.id - message.message_id)}.mp4'))
        user = message.from_user.get_mention(as_html=True)
        if message.chat.title:
            caption = f'👤 {user}\n\n🔗 <a href="{message.text}">{author}</a>\n\n📝 {title}'
        else:
            caption = f'👤 <a href="{message.text}">{author}</a>\n\n📝 {title}'
        video = InputFile(f'temp/{message.from_user.id - message.message_id}.mp4')
        await bot.send_video(chat_id=message.chat.id, video=video,
                            caption=caption)
        await bot.delete_message(message.chat.id, message.message_id)
        remove(f'temp/{message.from_user.id - message.message_id}.mp4')
    except:
        await message.answer('Ошибка. Повторите попытку.')


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtube.com/watch?v=') or message.text.startswith('https://youtu.be/'))
async def videos(message: types.Message):
    try:
        url = message.text
        patterns = [r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\&|\?)?", r"youtu\.be\/([0-9A-Za-z_-]{11})"]
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
                duration = isodate.parse_duration(json_data["contentDetails"]["duration"]).total_seconds()
        if int(duration) < 300:
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video.download(filename=f'temp/{message.from_user.id - message.message_id}.mp4')
            video = InputFile(f'temp/{message.from_user.id - message.message_id}.mp4')
            user = message.from_user.get_mention(as_html=True)
            if message.chat.title:
                caption = f'👤 {user}\n\n🔗 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            else:
                caption = f'👤 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            await bot.send_video(chat_id=message.chat.id, video=video,
                                caption=caption)
            await bot.delete_message(message.chat.id, message.message_id)
            remove(f'temp/{message.from_user.id - message.message_id}.mp4')
    except:
        await message.answer('Ошибка. Повторите попытку (Возможно видео недоступно).')

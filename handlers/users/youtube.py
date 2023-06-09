from os import remove
from aiogram import types

from loader import bot, dp
from utils.misc.throttling import rate_limit
from aiogram.types import InputFile

import aiohttp
import isodate
from data.config import YOUTUBE_API
import re

from service import youtube
from keyboards import inline_kp_youtube

from utils.logs import send_logs


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
    try:
        duration, author, title = await info_video(message.text)
        if int(duration) < 600:
            await youtube.download_video(message.text, message.from_user.id - message.message_id)
            user = message.from_user.get_mention(as_html=True)
            video = InputFile(
                f'temp/youtube_video_{message.from_user.id - message.message_id}.mp4')
            caption = f'👤 {user}\n\n🔗 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            await bot.send_video(chat_id=message.chat.id, video=video,
                                caption=caption)
            await bot.delete_message(message.chat.id, message.message_id)
            remove(
                f'temp/youtube_video_{message.from_user.id - message.message_id}.mp4')
    except Exception as ex:
        print(ex)
        await message.answer('Ошибка. Повторите попытку (Возможно видео недоступно).')
    await send_logs(message.from_user.first_name, message.text)


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtube.com/watch?v=') or message.text.startswith('https://youtu.be/') or message.text.startswith('https://www.youtube.com/shorts/') or message.text.startswith('https://youtube.com/shorts/'))
async def videos_private(message: types.Message):
    try:
        duration, author, title = await info_video(message.text)
        if int(duration) < 600:
            temp = await message.answer('Ожидайте...')
            await youtube.download_video(message.text, message.from_user.id - message.message_id)
            video = InputFile(f'temp/youtube_video_{message.from_user.id - message.message_id}.mp4')
            caption = f'👤 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            await bot.send_video(chat_id=message.chat.id, video=video,
                                caption=caption)
            await message.delete()
            await temp.delete()
            remove(f'temp/youtube_video_{message.from_user.id - message.message_id}.mp4')
    except Exception as ex:
        print(ex)
        await message.answer('Ошибка. Повторите попытку (Возможно видео недоступно).')
    await send_logs(message.from_user.first_name, message.text)

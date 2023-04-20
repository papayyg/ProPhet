import asyncio
from functools import partial
from os import remove

from aiogram import types
from pytube import YouTube

from loader import bot, dp
from utils.misc.throttling import rate_limit


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
        if message.chat.title:
            caption = f'👤 {message.from_user.first_name}\n\n🔗 <a href="{message.text}">{author}</a>\n\n📝 {title}'
        else:
            caption = f'👤 <a href="{message.text}">{author}</a>\n\n📝 {title}'
        video = open(f'temp/{message.from_user.id - message.message_id}.mp4', 'rb')
        await bot.send_video(chat_id=message.chat.id, video=video,
                            caption=caption)
        await bot.delete_message(message.chat.id, message.message_id)
        video.close()
    except:
        await message.answer('Ошибка. Повторите попытку.')
    remove(f'temp/{message.from_user.id - message.message_id}.mp4')


@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/watch?v=') or message.text.startswith('https://youtube.com/watch?v=') or message.text.startswith('https://youtu.be/'))
async def videos(message: types.Message):
    try:
        video_url = message.text
        loop = asyncio.get_event_loop()
        yt = await loop.run_in_executor(None, partial(YouTube, video_url))
        duration = yt.length
        author = yt.author
        title = yt.title
        if int(duration) < 210:
            stream = yt.streams.get_highest_resolution()
            await loop.run_in_executor(None, partial(stream.download, filename=f'temp/{str(message.from_user.id - message.message_id)}.mp4'))
            video = open(f'temp/{message.from_user.id - message.message_id}.mp4', 'rb')
            if message.chat.title:
                caption = f'👤 {message.from_user.first_name}\n\n🔗 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            else:
                caption = f'👤 <a href="{message.text}">{author}</a>\n\n📝 {title}'
            await bot.send_video(chat_id=message.chat.id, video=video,
                                caption=caption)
            await bot.delete_message(message.chat.id, message.message_id)
            video.close()
    except:
        await message.answer('Ошибка. Повторите попытку.')
    remove(f'temp/{message.from_user.id - message.message_id}.mp4')

from os import remove

from aiogram import types
from moviepy.editor import *

from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(limit=3)
@dp.message_handler(commands=['sound'], commands_prefix="/!@")
async def command_sound(message: types.Message):
    if message.reply_to_message and message.reply_to_message.video:
        file = await dp.bot.get_file(message.reply_to_message.video.file_id)
        file_path = file.file_path
        await dp.bot.download_file(file_path, f'temp/{message.from_user.id-message.message_id}.mp4')
        video = VideoFileClip(f"temp/{message.from_user.id-message.message_id}.mp4")
        audio = video.audio
        audio.write_audiofile(f"temp/{message.from_user.id-message.message_id}.mp3", logger=None)
        audio.close()
        video.close()
        audio = types.InputFile(f'temp/{message.from_user.id-message.message_id}.mp3')
        await dp.bot.send_audio(chat_id=message.chat.id, audio=audio,
                             reply_to_message_id=message.reply_to_message.message_id, title=f'{message.from_user.id-message.message_id}',
                             performer="ProPhet")
        remove(f"temp/{message.from_user.id-message.message_id}.mp4")
        remove(f"temp/{message.from_user.id-message.message_id}.mp3")
    else:
        await message.reply("Напишите сообщение ответом на видео")
from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from yandex_music import ClientAsync
from aiogram.types import InputFile
import re
from shazamio import Shazam

@rate_limit(limit=3)
@dp.message_handler(commands=['sz'], commands_prefix="/!@")
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
            await message.answer('Введите ответом на аудио/видео/голосовое сообщение/видеосообщение')
            return
        await dp.bot.download_file(file.file_path, f"temp/{message.from_user.id - message.message_id}.mp3")
        out = await shazam.recognize_song(f"temp/{message.from_user.id - message.message_id}.mp3")
        if len(out['matches']) == 0:
            await temp.edit_text('К сожалению, я не могу определить что за песня.')
            return
        await message.reply_photo(out["track"]["images"]["coverart"], f"<b>🎶 {out['track']['title']}\n🙎🏻‍♂️ {out['track']['subtitle']}</b>")
        await temp.delete()
        remove(f"temp/{message.from_user.id-message.message_id}.mp3")
    else:
        await message.answer('Введите ответом на аудио/видео/голосовое сообщение/видеосообщение')
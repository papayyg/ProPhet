from os import remove
from aiogram import types
from loader import bot, dp
from utils.misc.throttling import rate_limit
from yandex_music import ClientAsync
from aiogram.types import InputFile
import re
from shazamio import Shazam
from data.config import YANDEX_TOKEN

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
        temp = await bot.send_photo(message.chat.id, out["track"]["images"]["coverart"], caption, reply_to_message_id=message.reply_to_message.message_id)
        remove(f'temp/{message.from_user.id - message.message_id}.mp3')
        try:
            client = await ClientAsync(YANDEX_TOKEN).init()
            result = (await client.search(f"{out['track']['title']} {out['track']['subtitle']}")).best
            music_id = f'{result["result"]["id"]}:{result["result"]["albums"][0]["id"]}'
            short_track = (await client.tracks([music_id]))[0]
            title, artist = short_track['title'], short_track['artists'][0]['name']
            await short_track.download_async(f'temp/{message.from_user.id - message.message_id}.mp3')
            music = InputFile(f'temp/{message.from_user.id - message.message_id}.mp3')
            await bot.send_audio(message.chat.id, music, '🎧 <b><i>Яндекс.Музыка</i></b>', reply_to_message_id=temp.message_id, title=title, performer=artist)
            remove(f"temp/{message.from_user.id-message.message_id}.mp3")
        except:
            return
    else:
        await temp.edit_text('Введите ответом на аудио/видео/голосовое сообщение/видеосообщение')
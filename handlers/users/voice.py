from os import remove

from aiogram import types
from aiogram.types import InputFile
from googletrans import Translator
from gtts import gTTS

from loader import dp
from service import ai
from utils.misc.throttling import rate_limit

translator = Translator()

@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def voice_to_text(message: types.Message):
    if message.from_user.is_bot: return 0
    file = await dp.bot.get_file(message.voice.file_id)
    file_path = file.file_path
    file_id = f"temp/{message.from_user.id - message.message_id}"
    await dp.bot.download_file(file_path, f"{file_id}.ogg")
    answer = await ai.openai_audio(file_id, message.chat.id, message.message_id)
    if answer: await message.reply(answer)

@rate_limit(limit=3)
@dp.message_handler(commands=['ts'], commands_prefix="/!@")
async def text_to_speech(message: types.Message):
    text = message.reply_to_message.text if message.reply_to_message else message.text.split(' ', 1)[1]
    language = translator.detect(text).lang
    if type(language) == list: language = language[0]
    try:
        tts = gTTS(text, lang=language)
    except Exception as ex:
        return await message.reply(translator.translate(f'⚠️ {ex}', dest='ru').text)
    file_id = f"temp/{message.from_user.id - message.message_id}.ogg"
    tts.save(file_id)
    voice = InputFile(file_id)
    if message.reply_to_message: await dp.bot.send_voice(chat_id=message.chat.id, voice=voice, reply_to_message_id=message.reply_to_message.message_id)
    else: await message.reply_voice(voice=voice)
    remove(f"temp/{message.from_user.id - message.message_id}.ogg")

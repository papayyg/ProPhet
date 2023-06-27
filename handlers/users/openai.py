from os import remove

import aiohttp
from aiogram import types
from aiogram.types import InputFile, MediaGroup

from loader import bot, dp
from service.ai import openai_image, openai_turbo, openai_variation
from utils.misc.throttling import rate_limit

from utils.logs import send_logs

@rate_limit(limit=5)
@dp.message_handler(lambda message: (message.text.lower().startswith('бот,') or message.text.lower().startswith('bot,')) and len(message.text) > 4)
async def gpt_bot(message: types.Message):
    temp = await message.reply('Отправил запрос, ожидайте')
    try:
        gpt_answer = await openai_turbo(message.text[message.text.find(',')+1:].strip())
    except Exception as ex:
        gpt_answer = ex
    try:
        await temp.edit_text(gpt_answer, parse_mode='Markdown')
    except:
        gpt_answer.replace('<', '\\<')
        gpt_answer.replace('>', '\\>')
        await temp.edit_text(gpt_answer, parse_mode=None, disable_web_page_preview=True)
    await send_logs(message.from_user.first_name, message.text)

@rate_limit(limit=20)
@dp.message_handler(lambda message: (message.text.lower().startswith('фото,') or message.text.lower().startswith('image,')) and len(message.text) > 5)
async def gpt_image(message: types.Message):
    temp = await message.reply('Отправил запрос, ожидайте')
    data = await openai_image(message.text[message.text.find(',')+1:].strip())
    album = MediaGroup()
    for i in range(1):
        async with aiohttp.ClientSession() as session:
            async with session.get(data[i]["url"]) as response:
                photo_data = await response.read()
                filename = f"temp/image_{message.from_user.id}_{i}.jpg"
                with open(filename, "wb") as f:
                    f.write(photo_data)
        image = open(f"temp/image_{message.from_user.id}_{i}.jpg", 'rb')
        photo = InputFile(image)
        album.attach_photo(photo)
    await message.reply_media_group(album)
    await temp.delete()
    for i in range(1): remove(f"temp/image_{message.from_user.id}_{i}.jpg")
    await send_logs(message.from_user.first_name, message.text)

@rate_limit(limit=20)
@dp.message_handler(commands=['var'], commands_prefix="/!@", is_reply=True)
async def gpt_variation(message: types.Message):
    if message.reply_to_message.photo:
        temp = await message.reply('Отправил запрос, ожидайте')
        file = await bot.get_file(message.reply_to_message.photo[-1].file_id)
        await bot.download_file(file.file_path, f'temp/{message.chat.id - message.message_id}.png')
        data = await openai_variation(f'temp/{message.chat.id - message.message_id}.png')
        album = MediaGroup()
        for i in range(1):
            async with aiohttp.ClientSession() as session:
                async with session.get(data[i]["url"]) as response:
                    photo_data = await response.read()
                    filename = f"temp/image_{message.from_user.id}_{i}.jpg"
                    with open(filename, "wb") as f:
                        f.write(photo_data)
            image = open(f"temp/image_{message.from_user.id}_{i}.jpg", 'rb')
            photo = InputFile(image)
            album.attach_photo(photo)
        await message.reply_media_group(album)
        await temp.delete()
        for i in range(1): remove(f"temp/image_{message.from_user.id}_{i}.jpg")
    else:
        await message.reply('Напишите ответом на фото')
    await send_logs(message.from_user.first_name, message.text)

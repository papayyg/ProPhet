import asyncio
import base64
import io
import os

import aiohttp
from aiogram import types
from PIL import Image, PngImagePlugin

from data.config import dream, owner_id, real
from loader import bot, dp
from utils.misc.throttling import rate_limit

servers = {
    'dream': dream,
    'real': real
}

queue = asyncio.Queue()

async def process_queue():
    while True:
        prompt, chat_id, message_id, temp, server = await queue.get()
        await temp.edit_text('Обрабатываю ваш запрос')
        payload = {
            "prompt": prompt,
            "steps": 20,
            "sampler_index": "DPM++ SDE Karras",
            "width": 768,
            "height": 768,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=f'{server}/sdapi/v1/txt2img',
                        json=payload) as response:
                    r = await response.json()
                    for i in r['images']:
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
                        png_payload = {
                            "image": "data:image/png;base64," + i
                        }
                        async with session.post(
                                url=f'{server}/sdapi/v1/png-info',
                                json=png_payload) as response2:
                            pnginfo = PngImagePlugin.PngInfo()
                            t = await response2.json()
                            t = t.get("info")
                            pnginfo.add_text("parameters", t)
                            image.save('temp/output.png', pnginfo=pnginfo)
            photo = types.InputFile('temp/output.png')
            await bot.send_photo(chat_id, photo, reply_to_message_id=message_id)
            await temp.delete()
            os.remove('temp/output.png')
        except:
            await temp.edit_text('<i>Сервер недоступен.</i> Попробуйте другую модель.')
        queue.task_done()


async def on_startup_queue(dp):
    asyncio.create_task(process_queue())

@rate_limit(limit=15)
@dp.message_handler(commands=['dream'])
async def process_image_command(message: types.Message):
    queue_size = queue.qsize()
    temp = await message.reply(f'Запрос добавлен в очередь на {queue_size+1} месте')
    await queue.put((message.text[5:], message.chat.id, message.message_id, temp, servers['dream']))

@rate_limit(limit=15)
@dp.message_handler(commands=['real'])
async def process_image_command(message: types.Message):
    queue_size = queue.qsize()
    temp = await message.reply(f'Запрос добавлен в очередь на {queue_size+1} месте')
    await queue.put((message.text[5:], message.chat.id, message.message_id, temp, servers['real']))


@dp.message_handler(commands=['server_dream'], user_id=owner_id)
async def config_server_dream(message: types.Message):
    servers['dream'] = message.text.split()[1]
    await message.answer('<i>Сервер был успешно изменен!</i>')

@dp.message_handler(commands=['server_real'], user_id=owner_id)
async def config_server_real(message: types.Message):
    servers['real'] = message.text.split()[1]
    await message.answer('<i>Сервер был успешно изменен!</i>')
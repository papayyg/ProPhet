from io import BytesIO
from os import remove

import aiohttp
from PIL import Image
from pydub import AudioSegment

from data import config
from loader import dp


async def openai_turbo(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config.OPENAI_API_KEY,
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': text,
            },
        ],
        'temperature': 0.7
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://api.openai.com/v1/chat/completions', json=json_data) as response:
            response_json = await response.json()
            message = response_json["choices"][0]["message"]["content"]
    return message

async def openai_image(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config.OPENAI_API_KEY,
    }
    json_data = {
        'prompt': text,
        'n': 1,
        'size': '512x512',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://api.openai.com/v1/images/generations', json=json_data) as response:
            response_json = await response.json()
            message = response_json["data"]
    return message

async def openai_variation(path):
    headers = {
        'Authorization': 'Bearer ' + config.OPENAI_API_KEY,
    }

    image = Image.open(path)
    width, height = 512, 512
    image = image.resize((width, height))

    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    remove(f'{path[:-4]}.png')
    files = {
        'image': byte_array,
        'n': '1',
        'size': '512x512',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://api.openai.com/v1/images/variations', data=files) as response:
            response_json = await response.json()
            message = response_json["data"]
    return message

async def openai_audio(path, chat_id, message_id):
    audio = AudioSegment.from_ogg(f"{path}.ogg")
    audio.export(f"{path}.mp3", format="mp3")
    headers = {
        'Authorization': 'Bearer ' + config.OPENAI_API_KEY,
    }
    files = {
        'file': open(f"{path}.mp3", 'rb'),
        'model': 'whisper-1',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, data=files) as response:
            response_json = await response.json()
            answer = response_json['text']
    if answer[:3].lower() in ["bot", "бот", 'вот']:
        temp = await dp.bot.send_message(chat_id, 'Отправил запрос, ожидайте', reply_to_message_id=message_id)
        answer = await openai_turbo(answer[3:])
        await temp.edit_text(answer)
        answer = False
    try:
        remove(f"{path}.mp3")
        remove(f"{path}.ogg")
    except:
        remove(f"{path}.mp3")
        remove(f"{path}.ogg")
    return answer
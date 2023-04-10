import asyncio
import time

import aiohttp

from data import config
from handlers.users.image import servers


async def check_real():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f'{servers["real"]}') as response:
                r = await response.json()
                real = '🟢'
    except:
        real = '🔴'
    return real

async def check_dream():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f'{servers["dream"]}') as response:
                r = await response.json()
                dream = '🟢'
    except:
        dream = '🔴'
    return dream

async def check_weather():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q=baku&appid={config.OPEN_WEATHER}&units=metric') as r:
                data = await r.json()
                weather = '🟢'
    except:
        weather = '🔴'
    return weather

async def check_currency():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://v6.exchangerate-api.com/v6/{config.CURRENCY_API}/latest/AZ") as response:
                data = await response.json()
                weather = '🟢'
    except:
        weather = '🔴'
    return weather


async def check_openai():
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config.OPENAI_API_KEY,
        }
        json_data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'user',
                    'content': '5+5',
                },
            ],
            'temperature': 0.7
        }
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            start_time = time.time()
            async with session.post('https://api.openai.com/v1/chat/completions', json=json_data) as response:
                end_time = time.time()
                response_time = int(end_time - start_time)
    except:
        response_time = 0
    if not (0 < response_time < 60):
        open_ai = '🔴'
    elif response_time > 20:
        open_ai = '🟠'
    elif response_time > 10:
        open_ai = '🟡'
    else:
        open_ai = '🟢'
    return open_ai
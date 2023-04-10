from aiogram import types
from googletrans import Translator

from loader import dp
from service.weather import get_weather
from utils.misc.throttling import rate_limit

translator = Translator()

@rate_limit(limit=3)
@dp.message_handler(commands=['weather', 'погода'], commands_prefix="/!@")
async def weather_command(message: types.Message):
    city = 'baku'
    if ' ' in message.text:
        city = translator.translate(message.text[message.text.find(' ') + 1:], src='ru', dest='en').text
    try:
        await message.reply(await get_weather(city))
    except:
        await message.reply('Введите название города правильно (Через пробел)')
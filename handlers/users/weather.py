from aiogram import types
from googletrans import Translator

from loader import dp
from service.weather import get_weather
from utils.misc.throttling import rate_limit

translator = Translator()

from locales.translations import _
from utils.locales import locales_dict

@rate_limit(limit=3)
@dp.message_handler(commands=['weather', 'погода'], commands_prefix="/!@")
async def weather_command(message: types.Message):
    city = 'baku'
    if len(message.text.split()) != 1:
        city = translator.translate(message.text.split()[1], src='ru', dest='en').text
    try:
        await message.reply(await get_weather(city, message.chat.id))
    except:
        await message.reply(await _('Введите название города правильно (Через пробел)', locales_dict[message.chat.id]))
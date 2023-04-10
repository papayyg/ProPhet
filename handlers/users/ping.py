from aiogram import types

from loader import dp
from service import ping
from utils.misc.throttling import rate_limit


@rate_limit(limit=20)
@dp.message_handler(commands=['ping'], commands_prefix="/!@")
async def command_ping(message: types.Message):
    white = '⚪️'
    temp = await message.reply(f'<b><i>Статус серверов:</i>\n{white} OpenaAI\n{white} OpenWeather\n{white} CurrencyAPI\n{white} RealVision\n{white} DreamShaper</b>\n\n<i>Идет обработка...</i>')

    real = await ping.check_real()
    await temp.edit_text(f'<b><i>Статус серверов:</i>\n{white} OpenaAI\n{white} OpenWeather\n{white} CurrencyAPI\n{real} RealVision\n{white} DreamShaper</b>\n\n<i>Идет обработка..</i>')

    dream = await ping.check_dream()
    await temp.edit_text(f'<b><i>Статус серверов:</i>\n{white} OpenaAI\n{white} OpenWeather\n{white} CurrencyAPI\n{real} RealVision\n{dream} DreamShaper</b>\n\n<i>Идет обработка...</i>')

    weather = await ping.check_weather()
    await temp.edit_text(f'<b><i>Статус серверов:</i>\n{white} OpenaAI\n{weather} OpenWeather\n{white} CurrencyAPI\n{real} RealVision\n{dream} DreamShaper</b>\n\n<i>Идет обработка..</i>')

    currency = await ping.check_currency()
    await temp.edit_text(f'<b><i>Статус серверов:</i>\n{white} OpenaAI\n{weather} OpenWeather\n{currency} CurrencyAPI\n{real} RealVision\n{dream} DreamShaper</b>\n\n<i>Идет обработка...</i>')

    open_ai = await ping.check_openai()
    await temp.edit_text(f'<b><i>Статус серверов:</i>\n{open_ai} OpenaAI\n{weather} OpenWeather\n{currency} CurrencyAPI\n{real} RealVision\n{dream} DreamShaper</b>\n\n<i>Обработка завершена</i>')
    
import datetime

import aiohttp

from data.config import OPEN_WEATHER

from locales.translations import _
from utils.locales import locales_dict


async def get_weather(city, chat_id):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER}&units=metric') as r:
            data = await r.json()
            city = data['name']
            feels_temp = data['main']['feels_like']
            real_temp = data['main']['temp']
            weather_descr = data['weather'][0]['main']
            if weather_descr in code_to_smile:
                    wd = code_to_smile[weather_descr]
            else:
                    wd = 'Посмотри в окно'
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            length_of_the_day = datetime.datetime.fromtimestamp(
            data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            text = await _('\U0001F570 <b><i>{now}</i></b>\n<b>Погода в</b> <i>{city}</i>\n<b>Температура:</b> <i>{real_temp}C° <b>{wd}</b></i>\n\U0001F321 <b>Ощущение:</b> <i>{feels_temp}C°</i>\n\U0001F4A7 <b>Влажность:</b> <i>{humidity}%</i> \n\U0001F4A8	<b>Скорость ветра:</b> <i>{wind} м/c</i>\n\U0001F305 <b>Рассвет:</b> <i>{sunrise}</i>\n\U0001F307 <b>Закат:</b> <i>{sunset}</i>\n\U0001F304 <b>Продолжительность дня:</b> <i>{length}</i>', locales_dict[chat_id])
            return (text.format(now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), city=city, real_temp=real_temp, wd=wd, feels_temp=feels_temp, humidity=humidity, wind=wind, sunrise=sunrise_time.strftime("%H:%M:%S"), sunset=sunset_time.strftime("%H:%M:%S"), length=length_of_the_day))


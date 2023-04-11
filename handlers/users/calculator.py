import math
import re

from aiogram import types

from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(limit=1)
@dp.message_handler(commands=['c'], commands_prefix="/!@")
async def calculator(message: types.Message):
    if len(message.text.split()) == 1:
        await message.answer('Напишите выражение')
        return
    original_string = message.text[message.text.find(' ') + 1:]
    modified_string = re.sub(r'\b([a-z])', r'math.\g<1>', original_string)
    try:
        await message.reply(eval(modified_string))
    except Exception as ex:
        if str(ex) == "name 'math' is not defined":
            await message.reply(f"⚠️ Ошибка: <i>Использовано неверное выражение</i>")
        else: await message.reply(f"⚠️ Ошибка: <code>{ex}</code>")

@rate_limit(limit=5)
@dp.message_handler(commands=['c_help'], commands_prefix="/!@")
async def calculator_help(message: types.Message):
    await message.answer('''Обычные математические операции:
    "+" - Сложение 
    "-" - Вычитание 
    "*" - Умножение
    "/" - Деление
    "**" - Возведение в степень
    "%" - Остаток от деления
    "//" - Целочисленное деление

<a href="https://pythonworld.ru/moduli/modul-math.html">Функции</a> из модуля <b>math></b>:
    pi, e, sqrt(), log(), exp(), factorial(), sin(), cos(), fabs(), ceil() и т.д

<i>Пример использования:</i> sin(pi/2) ** 2 + 2 - factorial(3)''', disable_web_page_preview=True)
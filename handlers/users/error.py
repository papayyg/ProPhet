import datetime
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions
from googletrans import Translator

from data import config
from loader import dp

translator = Translator()

async def error_handler(message, exception):
    chat_id = config.log_channel
    user, name = message.chat.title if message.chat.title else message.chat.username, message.chat.first_name
    error_message = f"⚠️ <b>Произошла ошибка в чате @{user} {name}" \
                    f":</b> <code>{exception}</code>\nИнициатор: {message.text}"
    logging.warning(exception)
    try:
        await dp.bot.send_message(config.log_channel, error_message)
    except exceptions.ChatNotFound:
        logging.warning(f"Не удалось отправить сообщение об ошибке в чат {chat_id}: чат не найден")


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        await error_handler(update.message, exception)
        await dp.bot.send_message(update.message.chat.id, f'⚠️ Произошла Ошибка: {translator.translate(exception, dest="ru").text}')
    except:
        await error_handler(update.callback_query.message, exception)
        await dp.bot.send_message(update.callback_query.message.chat.id, f'⚠️ Произошла Ошибка: {translator.translate(exception, dest="ru").text}')
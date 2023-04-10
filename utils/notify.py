import logging

from aiogram import Dispatcher

from data.config import log_channel


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(log_channel, f'🔔 <b><i>Бот запущен!</i></b>')
    except Exception as err:
        logging.warning(err)

async def on_shutdown_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(log_channel, f'❌ <b><i>Бот остановлен!</i></b>')
    except Exception as err:
        logging.warning(err)

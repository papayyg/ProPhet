from loader import bot, dp
from data.config import log_channel
from aiogram import Dispatcher

async def send_logs(user, text):
    await dp.bot.send_message(log_channel, f'{user} - {text}', disable_web_page_preview=True)

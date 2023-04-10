from aiogram import types

from data.config import owner_id
from loader import dp
from utils.db.aiomysql import BotDB


@dp.message_handler(commands=['stats'], user_id=owner_id)
async def check_stats(message: types.Message):
    count_chats, count_unibook = await BotDB.chats_stat()
    await message.answer(f'<i>Подписчиков у бота:</i> <b>{count_chats[0][0]}</b>\n<i>Авторизаций в Unibook:</i> <b>{count_unibook[0][0]}</b>')

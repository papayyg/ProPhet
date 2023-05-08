from aiogram import types

from data.config import owner_id
from loader import dp
from utils.db.aiomysql import BotDB


@dp.message_handler(commands=['add'], user_id=owner_id)
async def add_headman(message: types.Message):
    user_id = message.text[5:]
    await BotDB.insert_headman(user_id)
    await message.answer('Юзер добавлен!')
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


async def tiktok_id_kb(id):
    tt_kb = InlineKeyboardMarkup(row_width=1)
    tt_kb.add(InlineKeyboardButton('Фото и музыку', callback_data=f'tt_photo:{id}'))
    tt_kb.add(InlineKeyboardButton('Рендер видео', callback_data=f'tt_video:{id}'))
    return tt_kb
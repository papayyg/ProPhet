from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from locales.translations import _
from utils.locales import locales_dict

async def tiktok_id_kb(id, chat_id):
    tt_kb = InlineKeyboardMarkup(row_width=1)
    tt_kb.add(InlineKeyboardButton(await _('Фото и музыку', locales_dict[chat_id]), callback_data=f'tt_photo:{id}'))
    tt_kb.add(InlineKeyboardButton(await _('Рендер видео 1', locales_dict[chat_id]), callback_data=f'tt_video_1:{id}'))
    tt_kb.add(InlineKeyboardButton(await _('Рендер видео 2 (Если что-то не так на видео в 1)', locales_dict[chat_id]), callback_data=f'tt_video_2:{id}'))
    return tt_kb
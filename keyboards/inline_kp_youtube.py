from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from locales.translations import _
from utils.locales import locales_dict

async def youtube_kb(id, chat_id):
    yt_kb = InlineKeyboardMarkup(row_width=1)
    video_button = InlineKeyboardButton(await _('📼 Видео', locales_dict[chat_id]), callback_data=f'yt_video:{id}')
    audio_button = InlineKeyboardButton(await _('🎧 Аудио', locales_dict[chat_id]), callback_data=f'yt_audio:{id}')
    yt_kb.row(video_button, audio_button)
    return yt_kb
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

lang_km = InlineKeyboardMarkup(row_width=1)
lang_km.add(InlineKeyboardButton('🇷🇺 Русский', callback_data=f'lang_ru_l'))
lang_km.add(InlineKeyboardButton('🇦🇿 Azərbaycan', callback_data=f'lang_az_l'))


lang_km_start = InlineKeyboardMarkup(row_width=1)
lang_km_start.add(InlineKeyboardButton('🇷🇺 Русский', callback_data=f'lang_ru_s'))
lang_km_start.add(InlineKeyboardButton('🇦🇿 Azərbaycan', callback_data=f'lang_az_s'))
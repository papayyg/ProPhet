from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


async def cinema_menu(page_num, pages, url, str):
    cinema_kb = InlineKeyboardMarkup(row_width=1)
    next_button = InlineKeyboardButton('>', callback_data=f'{str}_next:{page_num}')
    back_button = InlineKeyboardButton('<', callback_data=f'{str}_back:{page_num}')
    first_button = InlineKeyboardButton('<<', callback_data=f'{str}_first')
    last_button = InlineKeyboardButton('>>', callback_data=f'{str}_last')
    if 0 < page_num < len(pages) - 1:
        cinema_kb.row(first_button, back_button, next_button, last_button)
    if page_num == 0:
        cinema_kb.row(next_button, last_button)
    if page_num == len(pages) - 1:
        cinema_kb.row(first_button, back_button)
    cinema_kb.add(InlineKeyboardButton('Купить билет 🎟', url=url))
    cinema_kb.add(InlineKeyboardButton('Закрыть', callback_data='close'))
    return cinema_kb

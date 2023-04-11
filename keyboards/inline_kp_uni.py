from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


async def uni_menu(uni_kb, page_num, pages, unique, str):
    next_button = InlineKeyboardButton('Следующая', callback_data=f'{str}_next:{unique}_{page_num}')
    back_button = InlineKeyboardButton('Предыдущая', callback_data=f'{str}_back:{unique}_{page_num}')
    if 0 < page_num < len(pages) - 1:
        uni_kb.row(back_button, next_button)
    if page_num == 0:
        uni_kb.row(next_button)
    if page_num == len(pages) - 1:
        uni_kb.row(back_button)
    uni_kb.add(InlineKeyboardButton('Закрыть', callback_data='close'))
    return uni_kb

async def journal_menu(page_num, pages, unique, str):
    uni_kb = InlineKeyboardMarkup(row_width=1)
    return await uni_menu(uni_kb, page_num, pages, unique, str)

async def subjects_menu(page_num, pages, unique, str):
    unibook_kb = InlineKeyboardMarkup(row_width=1)
    subjects_button = InlineKeyboardButton('📎 Файлы предмета', callback_data=f'{str}_subj:{unique}_{page_num}')
    unibook_kb.row(subjects_button)
    return await uni_menu(unibook_kb, page_num, pages, unique, str)
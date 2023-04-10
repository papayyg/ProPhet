import io

import aiohttp
from aiogram import types

from keyboards import inline_kp_cinema
from loader import dp
from service import parkcinema
from utils.misc.throttling import rate_limit


@rate_limit(limit=20)
@dp.message_handler(commands=['parkcinema'], commands_prefix="/!@")
async def command_parkcinema(message: types.Message):
    temp = await message.answer('Ожидайте запроса, может занять до <i>30 секунд</i>.')
    global pages
    try:
        pages = await parkcinema.parse_parkcinema()
        await send_page(0, message.chat.id, None)
        await temp.delete()
    except:
        await temp.edit_text('⚠️ Ошибка. Повторите еще раз.')

async def send_page(page_num, chat_id, message_id=None):
    if page_num == -1: page_num = len(pages) - 1
    page = pages[page_num]
    parkcinema_kb = await inline_kp_cinema.cinema_menu(page_num, pages, page[2], 'pc')
    text = f'Страница {page_num+1} из {len(pages)}:\n\n{page[0]}'
    photo = page[1]
    async with aiohttp.ClientSession() as session:
        async with session.get(photo) as response:
            photo_bytes = io.BytesIO(await response.read())
    if message_id:
        await dp.bot.edit_message_media(media=types.input_media.InputMediaPhoto(photo_bytes), chat_id=chat_id, message_id=message_id)
        await dp.bot.edit_message_caption(caption=text, chat_id=chat_id, message_id=message_id, reply_markup=parkcinema_kb)
    else:
        await dp.bot.send_photo(chat_id=chat_id, photo=photo_bytes, caption=text, reply_markup=parkcinema_kb)

@dp.callback_query_handler(lambda c: c.data.startswith('pc_back:'))
async def back_page(callback_query: types.CallbackQuery):
    page_num = int(callback_query.data.split(':')[1]) - 1
    await send_page(page_num, callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('pc_next:'))
async def next_page(callback_query: types.CallbackQuery):
    page_num = int(callback_query.data.split(':')[1]) + 1
    await send_page(page_num, callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'pc_first')
async def first_page(callback_query: types.CallbackQuery):
    await send_page(0, callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'pc_last')
async def last_page(callback_query: types.CallbackQuery):
    await send_page(-1, callback_query.message.chat.id, callback_query.message.message_id)
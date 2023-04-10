from aiogram import types

from loader import dp


@dp.callback_query_handler(lambda c: c.data == 'close')
async def close_page(callback_query: types.CallbackQuery):
    await callback_query.answer('Пользователь закрыл сообщение', show_alert=False)
    await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
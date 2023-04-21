from aiogram import types

from data.config import log_channel
from loader import dp
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit

from keyboards.lang_kp import lang_km, lang_km_start
from states import language
from aiogram.dispatcher import FSMContext

from locales.translations import _
from utils.locales import locales_dict

from utils.commands import set_command_lang

async def start_cmd(message):
    await message.answer(await _('<b>Приветствую тебя, мой друг!</b> Я бот, созданный для того, чтобы <i>облегчить твою жизнь и сделать ее более продуктивной</i>. \n\nС моими возможностями ты можешь ознакомиться команду - /help', locales_dict[message.chat.id]))
    if not await BotDB.chats_exists(message.chat.id):
        await BotDB.add_chat(message.chat.id, message.from_user.first_name)        

@rate_limit(limit=5)
@dp.message_handler(commands=['start'], commands_prefix="/!@")
async def start_command(message: types.Message):
    if await BotDB.locales_exists(message.chat.id):
        await start_cmd(message)
    else:
        await message.reply('<b>Выберите язык, чтобы продолжить:\n\nDavam etmək üçün dil seçin:</b>', reply_markup=lang_km_start)
        await language.lang.set()

@rate_limit(limit=5)
@dp.message_handler(commands=['lang'], commands_prefix="/!@")
async def lang_command(message: types.Message):
    await message.reply('<b>Выберите язык, чтобы продолжить:\n\nDavam etmək üçün dil seçin:</b>', reply_markup=lang_km)
    await language.lang.set()

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'), state=language.lang)
async def state_edu(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(lang=callback_query.data.split('_')[1])
    data = await state.get_data()
    lang = data.get('lang')
    await state.finish()
    await BotDB.set_lang(callback_query.message.chat.id, lang)
    locales_dict[callback_query.message.chat.id] = lang
    await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await set_command_lang(dp, callback_query.message.chat.id, lang)
    await dp.bot.send_message(log_channel, f'🟣 {callback_query.message.reply_to_message.from_user.get_mention(as_html=True)} подписался на бота!')
    if callback_query.data.split('_')[2] == 's':
        await start_cmd(callback_query.message.reply_to_message)
    else:
        await callback_query.message.answer(await _('<b><i>Вы успешно сменили язык!</i></b>', lang))
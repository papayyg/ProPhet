import asyncio
import shutil
from data.config import log_channel

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import inline_kp_uni
from loader import dp
from service import unibook
from states import authorization
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from service import naa


@rate_limit(limit=3)
@dp.message_handler(commands=['auth', 'вход'], commands_prefix="/!@")
async def uni_auth(message: types.Message):
    if await BotDB.login_exists(message.from_user.id):
        await message.reply('<b>Вы уже в базе!</b> Используйте /del, чтобы удалить данные из базы.')
    else:
        uni_km = InlineKeyboardMarkup(row_width=1)
        uni_km.add(InlineKeyboardButton('🛢 ASOIU', callback_data=f'select_asoiu'))
        uni_km.add(InlineKeyboardButton('✈️ NAA', callback_data=f'select_naa'))
        await message.answer('Вы начали процесс сохранения логина и пароля. Укажите универ:', reply_markup=uni_km)
        await authorization.edu.set()

@dp.callback_query_handler(lambda c: c.data.startswith('select_'), state=authorization.edu)
async def state_edu(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(edu=callback_query.data.split('_')[1])
    await dp.bot.edit_message_text('<b>Введите логин от платформы указанного университета</b>:', callback_query.message.chat.id, callback_query.message.message_id)
    await authorization.login.set()

@dp.message_handler(state=authorization.login)
async def state_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer('<b>Теперь введите пароль:</b>')
    await authorization.password.set()

@dp.message_handler(state=authorization.password)
async def state_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    login = data.get('login')
    password = data.get('password')
    edu = data.get('edu')
    await state.finish()
    temp = await message.answer('Проверяю данные...')
    auth_func = unibook.try_auth if edu == 'asoiu' else naa.try_auth
    if await auth_func(login, password):
        await BotDB.add_login(message.from_user.id, login, password, edu)
        await temp.edit_text('<b><i>Авторизация прошла успешно!</i></b> Все функции доступны.')
    else:
        await temp.edit_text('<b><i>Данные введены неверно!</i></b> Повторите попытку.')

@rate_limit(limit=5)
@dp.message_handler(commands=['del', 'удалить'], commands_prefix="/!@")
async def uni_del(message: types.Message):
    if await BotDB.login_exists(message.from_user.id):
        await BotDB.remove_login(message.from_user.id)
        await message.reply('<b>Вы успешно удалены из базы!</b>')
    else:
        await message.reply('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')

@rate_limit(limit=20)
@dp.message_handler(commands=['nb', 'нб'], commands_prefix="/!@")
async def uni_nb(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')
    miss_func = unibook.miss if uni == 'asoiu' else naa.get_nb
    await temp.edit_text(text=await miss_func(login, password))
    if await BotDB.chats_exists(message.chat.id):
        await BotDB.chat_update(message.chat.id, message.from_user.first_name)
    else:
        await BotDB.add_chat(message.chat.id, message.from_user.first_name)
        await dp.bot.send_message(log_channel, f'🟣 {message.from_user.get_mention(as_html=True)} подписался на бота!')

@rate_limit(limit=60)
@dp.message_handler(commands=['gpas'], commands_prefix="/!@")
async def unibook_gpas(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')
    if uni == 'asoiu':
        await temp.edit_text(text=await unibook.summarys(login, password))
    else:
        await temp.edit_text('К сожалению на данный момент функция не доступна для вас.')

@rate_limit(limit=60)
@dp.message_handler(commands=['gpa'], commands_prefix="/!@")
async def unibook_gpa(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')
    if uni == 'asoiu':
        await temp.edit_text(text=await unibook.summary(login, password))
    else:
        await temp.edit_text('К сожалению на данный момент функция не доступна для вас.')

output_pages = {}
output_files = {}

async def reset_variable(unique, chat_id, message_id):
    output_pages.pop(unique)
    try:
        await dp.bot.delete_message(chat_id, message_id)
    except:
        return

async def start_reset_task(unique, chat_id, message_id):
    await asyncio.sleep(120)
    await reset_variable(unique, chat_id, message_id)

@rate_limit(limit=10)
@dp.message_handler(commands=['journal', 'журнал'], commands_prefix="/!@")
async def uni_journal(message: types.Message):
    user_id = message.from_user.id
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(user_id)
    else:
        return await temp.edit_text('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')
    full_func = unibook.full_info if uni == 'asoiu' else naa.get_journal
    pages = await full_func(login, password)
    if len(pages) == 0:
        await temp.edit_text('<b>Поздравляю!</b> У вас нет предметов.')
    elif len(pages) == 1:
        await temp.edit_text(pages[0])
    else:
        unique = message.chat.id - temp.message_id
        output_pages[unique] = pages
        await send_page(0, message.chat.id, unique)
        asyncio.create_task(start_reset_task(unique, message.chat.id, temp.message_id))

@rate_limit(limit=10)
@dp.message_handler(commands=['subjects', 'предметы'], commands_prefix="/!@")
async def unibook_subjects(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')
    if uni == 'asoiu':
        subjects_list, pages_files, obj_files = await unibook.subjects_info(login, password)
        if len(subjects_list) == 0:
            await temp.edit_text('<b>Поздравляю!</b> У вас нет предметов.')
        elif len(subjects_list) == 1:
            await temp.edit_text(subjects_list[0])
        else:
            unique = message.chat.id - temp.message_id
            output_pages[unique] = subjects_list
            output_files[unique] = pages_files, obj_files, [login, password]
            await send_page(0, message.chat.id, unique)
            asyncio.create_task(start_reset_task(unique, message.chat.id, temp.message_id))
    else:
        await temp.edit_text('К сожалению на данный момент функция не доступна для вас.')


async def send_page(page_num, chat_id, unique):
    if page_num == -1: page_num = len(output_pages[unique]) - 1
    page = output_pages[unique][page_num]
    if 'кредитов' in page:
        uni_kb = await inline_kp_uni.subjects_menu(page_num, output_pages[unique], unique, 'uni')
    else:
        uni_kb = await inline_kp_uni.journal_menu(page_num, output_pages[unique], unique, 'uni')
    text = f'Страница {page_num + 1} из {len(output_pages[unique])}:\n\n{page}'
    await dp.bot.edit_message_text(text, chat_id=chat_id, message_id=chat_id - unique, reply_markup=uni_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('uni_back:'))
async def back_page(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    unique = int(parts[1].split("_")[0])
    page_num = int(parts[1].split("_")[1]) - 1
    await send_page(page_num, callback_query.message.chat.id, unique)


@dp.callback_query_handler(lambda c: c.data.startswith('uni_next:'))
async def next_page(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    unique = int(parts[1].split("_")[0])
    page_num = int(parts[1].split("_")[1]) + 1
    await send_page(page_num, callback_query.message.chat.id, unique)

@dp.callback_query_handler(lambda c: c.data.startswith('uni_subj:'))
async def subjects_page(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    unique = int(parts[1].split("_")[0])
    page_num = int(parts[1].split("_")[1])
    markup_subjects = types.InlineKeyboardMarkup(row_width=1, )
    for el in output_files[unique][0][page_num]:
        file_id = el[0]
        file_name = el[1]
        markup_subjects.add(types.InlineKeyboardButton(f'{file_name}', callback_data=f'files:{unique}_{file_id}'))
    markup_subjects.add(types.InlineKeyboardButton("🔙 Назад", callback_data=f'back:{unique}_{page_num}'))
    await dp.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text='📝 Выберите нужный файл, чтобы скачать:', reply_markup=markup_subjects,
                                parse_mode='HTML')

@dp.callback_query_handler(lambda c: c.data.startswith('files:'))
async def files_download(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    unique = int(parts[1].split("_")[0])
    file_id = int(parts[1].split("_")[1])
    file_name = f'{output_files[unique][1][file_id]}.doc'
    await unibook.download_files(file_id, file_name, output_files[unique][2])
    try:
        doc = open(f'temp/{output_files[unique][2][0]}/{file_name}', 'rb')
        await dp.bot.send_document(callback_query.message.chat.id, doc)
        doc.close()
        shutil.rmtree(f'temp/{output_files[unique][2][0]}')
    except Exception as ex:
        print(ex)
        await dp.bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False, text='Файл пустой!')
    await dp.bot.answer_callback_query(callback_query_id=callback_query.id)
    return

@dp.callback_query_handler(lambda c: c.data.startswith('back:'))
async def back_kb(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    page_num = int(parts[1].split("_")[1])
    unique = int(parts[1].split("_")[0])
    await send_page(page_num, callback_query.message.chat.id, unique)
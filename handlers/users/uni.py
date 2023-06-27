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

from locales.translations import _
from utils.locales import locales_dict

from utils.logs import send_logs


@rate_limit(limit=3)
@dp.message_handler(commands=['auth', 'вход'], commands_prefix="/!@")
async def uni_auth(message: types.Message):
    if await BotDB.login_exists(message.from_user.id):
        await message.reply(await _('<b>Вы уже в базе!</b> Используйте /del, чтобы удалить данные из базы.', locales_dict[message.chat.id]))
    else:
        uni_km = InlineKeyboardMarkup(row_width=1)
        uni_km.add(InlineKeyboardButton('🛢 ASOIU', callback_data=f'select_asoiu'))
        uni_km.add(InlineKeyboardButton('✈️ NAA', callback_data=f'select_naa'))
        await message.answer(await _('Вы начали процесс сохранения логина и пароля. Укажите универ:', locales_dict[message.chat.id]), reply_markup=uni_km)
        await authorization.edu.set()

@dp.callback_query_handler(lambda c: c.data.startswith('select_'), state=authorization.edu)
async def state_edu(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(edu=callback_query.data.split('_')[1])
    await dp.bot.edit_message_text(await _('<b>Введите логин от платформы указанного университета</b>:', locales_dict[callback_query.message.chat.id]), callback_query.message.chat.id, callback_query.message.message_id)
    await authorization.login.set()

@dp.message_handler(state=authorization.login)
async def state_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer(await _('<b>Теперь введите пароль:</b>', locales_dict[message.chat.id]))
    await authorization.password.set()

@dp.message_handler(state=authorization.password)
async def state_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    login = data.get('login')
    password = data.get('password')
    edu = data.get('edu')
    await state.finish()
    try:
        temp = await message.answer(await _('Проверяю данные...', locales_dict[message.chat.id]))
        auth_func = unibook.try_auth if edu == 'asoiu' else naa.try_auth
        if await auth_func(login, password):
            await BotDB.add_login(message.from_user.id, login, password, edu)
            await temp.edit_text(await _('<b><i>Авторизация прошла успешно!</i></b> Все функции доступны.', locales_dict[message.chat.id]))
        else:
            await temp.edit_text(await _('<b><i>Данные введены неверно!</i></b> Повторите попытку.', locales_dict[message.chat.id]))
    except:
        await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
        return

@rate_limit(limit=5)
@dp.message_handler(commands=['del', 'удалить'], commands_prefix="/!@")
async def uni_del(message: types.Message):
    if await BotDB.login_exists(message.from_user.id):
        await BotDB.remove_login(message.from_user.id)
        await message.reply(await _('<b>Вы успешно удалены из базы!</b>', locales_dict[message.chat.id]))
    else:
        await message.reply(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))

@rate_limit(limit=20)
@dp.message_handler(commands=['nb', 'нб'], commands_prefix="/!@")
async def uni_nb(message: types.Message):
    temp = await message.reply(await _('Отправляю запрос, ожидайте...', locales_dict[message.chat.id]))
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
    miss_func = unibook.miss if uni == 'asoiu' else naa.get_nb
    try:
        await temp.edit_text(text=await miss_func(login, password))
    except:
        await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
        return

@rate_limit(limit=60)
@dp.message_handler(commands=['gpas'], commands_prefix="/!@")
async def unibook_gpas(message: types.Message):
    temp = await message.reply(await _('Отправляю запрос, этой займет немало времени, ожидайте...', locales_dict[message.chat.id]))
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
    if ' ' in message.text:
        text = message.text.split(' ')
        login = text[1]
        password = text[2]
    if uni == 'asoiu':
        try:
            await temp.edit_text(text=await unibook.summarys(login, password, message.chat.id))
        except:
            await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
            return
    else:
        await temp.edit_text(await _('К сожалению на данный момент функция не доступна для вас.', locales_dict[message.chat.id]))
    await send_logs(message.from_user.first_name, message.text)

@rate_limit(limit=60)
@dp.message_handler(commands=['gpa'], commands_prefix="/!@")
async def unibook_gpa(message: types.Message):
    temp = await message.reply(await _('Отправляю запрос, этой займет немало времени, ожидайте...', locales_dict[message.chat.id]))
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
    if ' ' in message.text:
        text = message.text.split(' ')
        login = text[1]
        password = text[2]
    if uni == 'asoiu':
        try:
            await temp.edit_text(text=await unibook.summary(login, password, message.chat.id))
        except:
            await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
            return
    else:
        await temp.edit_text(await _('К сожалению на данный момент функция не доступна для вас.', locales_dict[message.chat.id]))
    await send_logs(message.from_user.first_name, message.text)

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

@rate_limit(limit=2)
@dp.message_handler(commands=['journal', 'журнал'], commands_prefix="/!@")
async def uni_journal(message: types.Message):
    user_id = message.from_user.id
    temp = await message.reply(await _('Отправляю запрос, ожидайте...', locales_dict[message.chat.id]))
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(user_id)
    else:
        return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
    if ' ' in message.text:
        text = message.text.split(' ')
        login = text[1]
        password = text[2]
    full_func = unibook.full_info if uni == 'asoiu' else naa.get_journal
    try:
        pages = await full_func(login, password, message.chat.id)
    except:
        await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
        return
    if len(pages) == 0:
        await temp.edit_text(await _('<b>Поздравляю!</b> У вас нет предметов.', locales_dict[message.chat.id]))
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
    temp = await message.reply(await _('Отправляю запрос, ожидайте...', locales_dict[message.chat.id]))
    if await BotDB.login_exists(message.from_user.id):
        login, password, uni = await BotDB.get_login(message.from_user.id)
    else:
        return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
    if uni == 'asoiu':
        # try:
        subjects_list, pages_files, obj_files = await unibook.subjects_info(login, password, message.chat.id)
        # except:
        #     await temp.edit_text('Ошибка подключения. Повторите попытку')
        #     return
        if len(subjects_list) == 0:
            await temp.edit_text(await _('<b>Поздравляю!</b> У вас нет предметов.', locales_dict[message.chat.id]))
        elif len(subjects_list) == 1:
            await temp.edit_text(subjects_list[0])
        else:
            unique = message.chat.id - temp.message_id
            output_pages[unique] = subjects_list
            output_files[unique] = pages_files, obj_files, [login, password]
            await send_page(0, message.chat.id, unique)
            asyncio.create_task(start_reset_task(unique, message.chat.id, temp.message_id))
    else:
        await temp.edit_text(await _('К сожалению на данный момент функция не доступна для вас.', locales_dict[message.chat.id]))


@rate_limit(limit=10)
@dp.message_handler(commands=['nball'], commands_prefix="/!@")
async def command_allnb(message: types.Message):
    if await BotDB.headman_exists(message.from_user.id):
        temp = await message.reply(await _('Отправляю запрос, ожидайте...', locales_dict[message.chat.id]))
        if await BotDB.login_exists(message.from_user.id):
            login, password, uni = await BotDB.get_login(message.from_user.id)
        else:
            try:
                login, password, uni = message.text.split(' ')[1], message.text.split(' ')[2], 'asoiu'
            except:
                return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
        if uni == 'asoiu':
            try:
                pages = await unibook.get_all_nb(login, password)
                unique = message.chat.id - temp.message_id
                output_pages[unique] = pages
                await send_page(0, message.chat.id, unique)
                asyncio.create_task(start_reset_task(unique, message.chat.id, temp.message_id))
            except Exception as ex:
                await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
                return
        else:
            await temp.edit_text(await _('К сожалению на данный момент функция не доступна для вас.', locales_dict[message.chat.id]))


@rate_limit(limit=10)
@dp.message_handler(commands=['journalall'], commands_prefix="/!@")
async def command_allnb(message: types.Message):
    if await BotDB.headman_exists(message.from_user.id):
        temp = await message.reply(await _('Отправляю запрос, ожидайте...', locales_dict[message.chat.id]))
        if await BotDB.login_exists(message.from_user.id) and ' ' not in message.text:
            login, password, uni = await BotDB.get_login(message.from_user.id)
        else:
            try:
                login, password, uni = message.text.split(' ')[1], message.text.split(' ')[2], 'asoiu'
            except:
                return await temp.edit_text(await _('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.', locales_dict[message.chat.id]))
        if uni == 'asoiu':
            try:
                pages = await unibook.get_all_journal(login, password, message.chat.id)
                unique = message.chat.id - temp.message_id
                output_pages[unique] = pages
                await send_page(0, message.chat.id, unique)
                asyncio.create_task(start_reset_task(unique, message.chat.id, temp.message_id))
            except Exception as ex:
                print(ex)
                await temp.edit_text(await _('Ошибка подключения. Повторите попытку', locales_dict[message.chat.id]))
                return
        else:
            await temp.edit_text(await _('К сожалению на данный момент функция не доступна для вас.', locales_dict[message.chat.id]))

async def send_page(page_num, chat_id, unique):
    if page_num == -1: page_num = len(output_pages[unique]) - 1
    page = output_pages[unique][page_num]
    if 'кредитов' in page or 'Kreditlərin' in page:
        uni_kb = await inline_kp_uni.subjects_menu(page_num, output_pages[unique], unique, 'uni', chat_id)
    else:
        uni_kb = await inline_kp_uni.journal_menu(page_num, output_pages[unique], unique, 'uni', chat_id)
    temp_text = await _('Страница {page_num} из {output_pages}:\n\n{page}', locales_dict[chat_id])
    text = temp_text.format(page_num=page_num + 1, output_pages=len(output_pages[unique]), page=page)
    await dp.bot.edit_message_text(text, chat_id=chat_id, message_id=chat_id - unique, reply_markup=uni_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('uni_back:'))
async def back_page(callback_query: types.CallbackQuery):
    try:
        parts = callback_query.data.split(":")
        unique = int(parts[1].split("_")[0])
        page_num = int(parts[1].split("_")[1]) - 1
        await send_page(page_num, callback_query.message.chat.id, unique)
    except:
        await callback_query.answer('Ошибка. Повторите попытку', show_alert=False)
        await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data.startswith('uni_next:'))
async def next_page(callback_query: types.CallbackQuery):
    try:
        parts = callback_query.data.split(":")
        unique = int(parts[1].split("_")[0])
        page_num = int(parts[1].split("_")[1]) + 1
        await send_page(page_num, callback_query.message.chat.id, unique)
    except:
        await callback_query.answer('Ошибка. Повторите попытку', show_alert=False)
        await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('uni_subj:'))
async def subjects_page(callback_query: types.CallbackQuery):
    try:
        parts = callback_query.data.split(":")
        unique = int(parts[1].split("_")[0])
        page_num = int(parts[1].split("_")[1])
        markup_subjects = types.InlineKeyboardMarkup(row_width=1, )
        for el in output_files[unique][0][page_num]:
            file_id = el[0]
            file_name = el[1]
            markup_subjects.add(types.InlineKeyboardButton(f'{file_name}', callback_data=f'files:{unique}_{file_id}'))
        markup_subjects.add(types.InlineKeyboardButton(await _("🔙 Назад", locales_dict[callback_query.message.chat.id]), callback_data=f'back:{unique}_{page_num}'))
        await dp.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                    text=await _('📝 Выберите нужный файл, чтобы скачать:', locales_dict[callback_query.message.chat.id]), reply_markup=markup_subjects)
    except:
        await callback_query.answer('Ошибка. Повторите попытку', show_alert=False)
        await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('files:'))
async def files_download(callback_query: types.CallbackQuery):
    try:
        parts = callback_query.data.split(":")
        unique = int(parts[1].split("_")[0])
        file_id = int(parts[1].split("_")[1])
        file_name = f'{output_files[unique][1][file_id]}.doc'
        try:
            await unibook.download_files(file_id, file_name, output_files[unique][2])
        except:
            await callback_query.message.answer(await _('Ошибка подключения. Повторите попытку', locales_dict[callback_query.message.chat.id]))
            return
        try:
            doc = open(f'temp/{output_files[unique][2][0]}/{file_name}', 'rb')
            await dp.bot.send_document(callback_query.message.chat.id, doc)
            doc.close()
            shutil.rmtree(f'temp/{output_files[unique][2][0]}')
        except Exception as ex:
            print(ex)
            await dp.bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False, text=await _('Файл пустой!', locales_dict[callback_query.message.chat.id]))
        await dp.bot.answer_callback_query(callback_query_id=callback_query.id)
        return
    except:
        await callback_query.answer('Ошибка. Повторите попытку', show_alert=False)
        await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('back:'))
async def back_kb(callback_query: types.CallbackQuery):
    try:
        parts = callback_query.data.split(":")
        page_num = int(parts[1].split("_")[1])
        unique = int(parts[1].split("_")[0])
        await send_page(page_num, callback_query.message.chat.id, unique)
    except:
        await callback_query.answer('Ошибка. Повторите попытку', show_alert=False)
        await dp.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
import asyncio
import shutil

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import inline_kp_unibook
from loader import dp
from service import unibook
from states import authorization
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit


@rate_limit(limit=10)
@dp.message_handler(commands=['auth', 'вход'], commands_prefix="/!@")
async def unibook_auth(message: types.Message):
    if await BotDB.login_exists(message.from_user.id):
        await message.reply('<b>Вы уже в базе!</b> Используйте /del, чтобы удалить данные из базы.')
    else:
        await message.answer('Вы начали процесс сохранения логина и пароля. Сперва отправьте логин:')
        await authorization.login.set()

@dp.message_handler(state=authorization.login)
async def state_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer('Теперь отправьте пароль:')
    await authorization.password.set()


@dp.message_handler(state=authorization.password)
async def state_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    login = data.get('login')
    password = data.get('password')
    await state.finish()
    temp = await message.answer('Проверяю данные...')
    if await unibook.try_auth(login, password):
        await BotDB.add_login(message.from_user.id, login, password)
        await temp.edit_text('<b><i>Авторизация прошла успешно!</i></b> Более не требуется ввод пароля.')
    else:
        await temp.edit_text('<b><i>Данные введены неверно!</i></b> Повторите попытку.')

@rate_limit(limit=5)
@dp.message_handler(commands=['del', 'удалить'], commands_prefix="/!@")
async def unibook_del(message: types.Message):
    if await BotDB.login_exists(message.from_user.id):
        await BotDB.remove_login(message.from_user.id)
        await message.reply('<b>Вы успешно удалены из базы!</b>')
    else:
        await message.reply('<b>Вас нет в базе!</b> Используйте /auth, чтобы авторизоваться.')

@rate_limit(limit=20)
@dp.message_handler(commands=['nb', 'нб'], commands_prefix="/!@")
async def unibook_nb(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if ' ' not in message.text:
        if await BotDB.login_exists(message.from_user.id):
            login, password = await BotDB.get_login(message.from_user.id)
        else:
            return await temp.edit_text(
                '<b>Вас нет в базе!</b> Напишите логин и пароль или сперва используйте <i>/auth</i>')
    else:
        login, password = await unibook.logpass(message.text)
    try:
        await temp.edit_text(text=await unibook.miss(login, password))
    except:
        await temp.edit_text(text='Неправильный логин или пароль')

@rate_limit(limit=60)
@dp.message_handler(commands=['gpas'], commands_prefix="/!@")
async def unibook_gpas(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if message.text[1:5].lower() == 'gpas' and ' ' not in message.text:
        if await BotDB.login_exists(message.from_user.id):
            login, password = await BotDB.get_login(message.from_user.id)
        else:
            await temp.edit_text('Вас нет в базе, напишите логин и пароль или сперва используйте <i>/auth</i>')
    else:
        login, password = await unibook.logpass(message.text)
    try:
        result = await unibook.summarys(login, password)
        await temp.edit_text(text=result)
    except:
        await temp.edit_text(text='Неправильный логин или пароль')

@rate_limit(limit=60)
@dp.message_handler(commands=['gpa'], commands_prefix="/!@")
async def unibook_gpa(message: types.Message):
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if message.text[1:4].lower() == 'gpa' and ' ' not in message.text:
        if await BotDB.login_exists(message.from_user.id):
            login, password = await BotDB.get_login(message.from_user.id)
        else:
            await temp.edit_text('Вас нет в базе, напишите логин и пароль или сперва используйте <i>/auth</i>')
    else:
        login, password = await unibook.logpass(message.text)
    try:
        result = await unibook.summary(login, password)
        await temp.edit_text(text=result)
    except:
        await temp.edit_text(text='Неправильный логин или пароль')


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
async def unibook_journal(message: types.Message):
    text = message.text
    user_id = message.from_user.id
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if ' ' not in text:
        if await BotDB.login_exists(user_id):
            login, password = await BotDB.get_login(user_id)
        else:
            await temp.edit_text('Вас нет в базе, напишите логин и пароль или сперва используйте <i>/auth</i>')
    else:
        login, password = await unibook.logpass(text)
    try:
        pages = await unibook.full_info(login, password)
        if len(pages) == 0:
            await temp.edit_text('<b>Поздравляю!</b> У вас нет предметов.')
        elif len(pages) == 1:
            await temp.edit_text(pages[0])
        else:
            unique = message.chat.id - temp.message_id
            output_pages[unique] = pages
            await send_page(0, message.chat.id, unique)
            asyncio.create_task(start_reset_task(unique, message.chat.id, temp.message_id))
    except Exception as ex:
        await temp.edit_text(text='Неправильный логин или пароль')

@rate_limit(limit=10)
@dp.message_handler(commands=['subjects', 'предметы'], commands_prefix="/!@")
async def unibook_subjects(message: types.Message):
    text = message.text
    user_id = message.from_user.id
    temp = await message.reply('Отправляю запрос, ожидайте...')
    if (text[1:9] == 'subjects' or text[1:9] == 'предметы') and ' ' not in text:
        if await BotDB.login_exists(user_id):
            login, password = await BotDB.get_login(user_id)
        else:
            await temp.edit_text('Вас нет в базе, напишите логин и пароль или сперва используйте <i>save</i>',
                                 parse_mode='HTML')
    else:
        login, password = await unibook.logpass(text)
    try:
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
    except Exception as ex:
        print(ex)
        await temp.edit_text(text='Неправильный логин или пароль')


async def send_page(page_num, chat_id, unique):
    if page_num == -1: page_num = len(output_pages[unique]) - 1
    page = output_pages[unique][page_num]
    if 'кредитов' in page:
        unibook_kb = await inline_kp_unibook.subjects_menu(page_num, output_pages[unique], unique, 'unibook')
    else:
        unibook_kb = await inline_kp_unibook.journal_menu(page_num, output_pages[unique], unique, 'unibook')
    text = f'Страница {page_num + 1} из {len(output_pages[unique])}:\n\n{page}'
    await dp.bot.edit_message_text(text, chat_id=chat_id, message_id=chat_id - unique, reply_markup=unibook_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('unibook_back:'))
async def back_page(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    unique = int(parts[1].split("_")[0])
    page_num = int(parts[1].split("_")[1]) - 1
    await send_page(page_num, callback_query.message.chat.id, unique)


@dp.callback_query_handler(lambda c: c.data.startswith('unibook_next:'))
async def next_page(callback_query: types.CallbackQuery):
    parts = callback_query.data.split(":")
    unique = int(parts[1].split("_")[0])
    page_num = int(parts[1].split("_")[1]) + 1
    await send_page(page_num, callback_query.message.chat.id, unique)

@dp.callback_query_handler(lambda c: c.data.startswith('unibook_subj:'))
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
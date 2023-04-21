from aiogram import types

from data.config import owner_id
from loader import dp
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit

from utils.contest import contest_schedule


@dp.message_handler(commands=['runqueer'], user_id=owner_id)
async def contest_run(message: types.Message):
    await contest_schedule(dp)

@rate_limit(limit=5)
@dp.message_handler(chat_type=["group", "supergroup"], is_admin=True, commands=['queer'], commands_prefix="/!@")
async def contest_on(message: types.Message):
    if await BotDB.check_pidor(message.chat.id) == 0:
        if await BotDB.check_chat(message.chat.id):
            await BotDB.add_pidor(message.chat.id)
            await message.reply('Теперь вы участвуете в ежедневном конкурсе! (Чтобы покинуть, введите команду повторно)')
        else:
            await message.reply('Сперва используйте /in')
    else:
        await BotDB.remove_pidor(message.chat.id)
        await message.reply('Вы больше не участвуете в конкурсе')

@rate_limit(limit=5)
@dp.message_handler(commands=['queer', 'pidor'], chat_type=["group", "supergroup"], commands_prefix="/!@")
async def contest(message: types.Message):
    await message.answer('Вы не администратор группы')

@rate_limit(limit=5)
@dp.message_handler(chat_type=["group", "supergroup"], commands=['queerstats', 'pidorstats'], commands_prefix="/!@")
async def contest_stats(message: types.Message):
    result = await BotDB.pidor_stats(message.chat.id)
    l = 'Топ-10 пидоров чата:\n\n'
    if len(result) <= 10:
        i = 1
        for user in result:
            l += f'{i}. {user[0]} — <i>{user[1]} раз(а)</i>\n'
            i += 1
    else:
        for i, user in enumerate(result):
            l += f'{i+1}. {user[i][0]} — <i>{user[i][1]} раз(а)</i>\n'
    if l == 'Топ-10 пидоров чата:\n\n':
        l += 'Их нет'
    await message.answer(l)

@rate_limit(limit=5)
@dp.message_handler(commands=['in', 'out', 'queer', 'all', 'queerstats'], commands_prefix = "/!@")
async def only_for_group_command(message: types.Message):
    await message.answer('Команду можно использовать только в группе')
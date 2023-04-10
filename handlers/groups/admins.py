import re
import time

from aiogram import types

from loader import bot, dp


@dp.message_handler(chat_type=["group", "supergroup"], commands=['kick', 'кик'], commands_prefix="/!@", is_admin=True)
async def kick_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    admin_name = message.from_user.get_mention(as_html=True)
    causer = message.reply_to_message.from_user.get_mention(as_html=True)
    if len(message.text.split()) == 1:
        comment = ''
    else:
        comment = " ".join(message.text.split()[1:])
    await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    if comment != '':
        await message.reply(f'🟠 {admin_name} <i>кикнул</i> {causer}! <b>Причина:</b> {comment}')
    else:
        await message.reply(f'🟠 {admin_name} <i>кикнул</i> {causer}!')

@dp.message_handler(chat_type=["group", "supergroup"], commands=['ban', 'бан'], commands_prefix="/!@", is_admin=True)
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    admin_name = message.from_user.get_mention(as_html=True)
    causer = message.reply_to_message.from_user.get_mention(as_html=True)
    if len(message.text.split()) == 1:
        comment = ''
    else:
        comment = " ".join(message.text.split()[1:])
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, )
    if comment != '':
        await message.reply(f'🔴 {admin_name} <i>забанил</i> {causer}! <b>Причина:</b> {comment}')
    else:
        await message.reply(f'🔴 {admin_name} <i>забанил</i> {causer}!')

@dp.message_handler(chat_type=["group", "supergroup"], commands=['unban', 'анбан'], commands_prefix="/!@", is_admin=True)
async def unban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    admin_name = message.from_user.get_mention(as_html=True)
    causer = message.reply_to_message.from_user.get_mention(as_html=True)
    await bot.unban_chat_member(chat_id=message.chat.id,
                                   user_id=message.reply_to_message.from_user.id)
    await message.reply(f"🔵 {admin_name} <i>разбанил</i> {causer}!")


@dp.message_handler(chat_type=["group", "supergroup"], commands=['mute', 'мут'], commands_prefix="/!@", is_admin=True)
async def mute_user(message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    admin_name = message.from_user.get_mention(as_html=True)
    causer = message.reply_to_message.from_user.get_mention(as_html=True)
    descr = message.text.split()
    try:
        if len(descr) == 1:
            time_mute = 600
            comment = ''
        elif len(descr) == 2 and descr[1].isdigit():
            time_mute = int(descr[1]) * 60
            comment = ''
        elif len(descr) == 2:
            time_mute = 600
            comment = descr[1]
        elif len(descr) >= 3:
            time_mute = int(re.findall(r'\d+', ' '.join(descr[1:]))[0]) * 60
            comment = re.findall(r'\D+', ' '.join(descr[1:]))[0].strip()
    except:
        await message.answer(f'Вы ввели неправильно аргументы!')
        return
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False),
                                        until_date=time.time()+time_mute)
    if comment != '':
        await message.answer(f'🟡 {admin_name} замутил {causer} <u>на {int(time_mute/60)} минут</u>! <b>Причина:</b> {comment}.')
    else:
        await message.answer(f'🟡 {admin_name} замутил {causer} <u>на {int(time_mute/60)} минут</u>!')

@dp.message_handler(chat_type=["group", "supergroup"], commands=['unmute', 'анмут'], commands_prefix="/!@", is_admin=True)
async def unmute_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    admin_name = message.from_user.get_mention(as_html=True)
    causer = message.reply_to_message.from_user.get_mention(as_html=True)
    await bot.restrict_chat_member(chat_id=message.chat.id,
                                   user_id=message.reply_to_message.from_user.id,
                                   permissions=types.ChatPermissions(True, True, True, True, True, True ,True ,True ,True ,True ,True ,True ,True))
    await message.reply(f"🟢 {admin_name} <i>размутил</i> {causer}!")


@dp.message_handler(chat_type=["group", "supergroup"], commands=['purge', 'пурге'], commands_prefix="/!@", is_admin=True)
async def mute_user(message):
    if message.reply_to_message:
        for i in range(message.message_id, message.reply_to_message.message_id, -1):
            try:
                await bot.delete_message(message.chat.id, i)
            except:
                continue
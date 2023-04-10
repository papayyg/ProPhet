from os import remove

from aiogram import types
from aiogram.types import InputFile
from PIL import Image

from data.config import bot_name
from loader import bot, dp
from service.drawer.drawer import BubbleDrawer


@dp.message_handler(commands=['qbs'], commands_prefix="/!@")
async def add_sticker(message: types.Message):
    if message.chat.title:
        name = message.chat.title
        stick_id = str(message.chat.id)[1:]
    else:
        name = message.chat.first_name
        stick_id = str(message.chat.id)
    if not message.reply_to_message:
        await message.answer('Отправьте команду ответом на фото/стикер/текстовое сообщение')
        return 0
    if message.reply_to_message.photo:
        file = await bot.get_file(message.reply_to_message.photo[-1].file_id)
        file_path = file.file_path
        await bot.download_file(file_path, f'temp/{message.chat.id}.png')
        im = Image.open(f"temp/{message.chat.id}.png")
        im = im.resize((512, 512))
        im.save(f"temp/{message.chat.id}.png")
        png = InputFile(f'temp/{message.chat.id}.png')
    elif message.reply_to_message.sticker:
        png = message.reply_to_message.sticker.file_id
    elif message.reply_to_message.text:
        b = BubbleDrawer(message.reply_to_message)
        result = await bot.get_user_profile_photos(message.reply_to_message.from_user.id, limit=1)
        if result.total_count > 0:
            file = await bot.get_file(result.photos[0][0].file_id)
            file_path = file.file_path
            await bot.download_file(file_path, f'temp/{message.chat.id}.png')
            b.set_avatar(f'temp/{message.chat.id}.png')
        try: b.draw()
        except:
            await message.reply('Сообщение слишком длинное')
            return
        b.save(f'temp/{message.chat.id}.png')
        png = InputFile(f'temp/{message.chat.id}.png')
    else:
        await message.reply('Работает только с текстом, фото и стикером')
        return
    try:
        await bot.get_sticker_set(f'Stickers_{stick_id}_by_{bot_name}')
        await bot.add_sticker_to_set(message.from_user.id, f'Stickers_{stick_id}_by_{bot_name}', '😂', png)
    except:
        await bot.create_new_sticker_set(message.from_user.id, f'Stickers_{stick_id}_by_{bot_name}', f'{name} pack by @{bot_name}', '😂', png)
    sticker_set = await bot.get_sticker_set(f'Stickers_{stick_id}_by_{bot_name}')
    await message.reply_sticker(sticker_set.stickers[-1].file_id)
    try:
        remove(f'temp/{message.chat.id}.png')
    except:
        return

@dp.message_handler(commands=['dbs'], commands_prefix="/!@")
async def delete_sticker(message: types.Message):
    try:
        await bot.delete_sticker_from_set(message.reply_to_message.sticker.file_id)
        await message.reply('Стикер успешно удален')
    except Exception as ex:
        await message.reply(f'⚠️ Ошибка: {ex}')
import os
import shutil

from aiogram import types

from data.config import owner_id
from loader import dp


@dp.message_handler(commands=['temp_look'], user_id=owner_id)
async def temp_look(message: types.Message):
    files = os.listdir('temp/')
    files_string = "\n".join(files)
    if files_string == '':
        files_string = '<b><i>*Пусто*</i></b>'
    await message.answer(f'Содержимое папки <b>temp</b>:\n{files_string}')


@dp.message_handler(commands=['temp_del'], user_id=owner_id)
async def temp_look(message: types.Message):
    for file in os.listdir('temp/'):
        file_path = os.path.join('temp/', file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except:
            continue

    for folder in os.listdir('temp/'):
        folder_path = os.path.join('temp/', folder)
        try:
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
        except:
            continue
    await message.answer('<b>Все файлы удалены успешно</b>')
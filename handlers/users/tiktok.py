import os
from urllib.parse import urlparse

from aiogram import types
from aiogram.types import InputFile, MediaGroup

from keyboards.inline_kp_tt import tiktok_id_kb
from loader import dp
from service import region, tiktok
from utils.misc.throttling import rate_limit

from locales.translations import _
from utils.locales import locales_dict


@rate_limit(limit=5)
@dp.message_handler(lambda message: (message.text.startswith('https://www.tiktok.com/') and '/t/' in message.text) or message.text.startswith('https://vt.tiktok') or (message.text.startswith('https://www.tiktok.com/') and 'video' in message.text), chat_type=["group", "supergroup"])
async def tiktok_download(message: types.Message):
    try:
        user = message.from_user.get_mention(as_html=True)
        if await tiktok.check_slide(message.text):
            if await region.baku():
                vide_id = "/".join(urlparse(message.text).path.split("/")[1:])
                tt_kb = await tiktok_id_kb(vide_id, message.chat.id)
                await message.reply(await _('<b>Вы отправили слайд-шоу</b>. Как вы хотите скачать?', locales_dict[message.chat.id]), reply_markup=tt_kb)
            else:
                author, text, shortlink, audio, descr_second = await tiktok_slide_download(message, message.text, 'group')
                await dp.bot.send_audio(chat_id=message.chat.id, audio=audio,
                                        caption=f'👤 {user}\n\n🔗 {shortlink}',
                                        performer=author, title=author)
                await dp.bot.delete_message(message.chat.id, message.message_id)
                await tiktok.tiktok_del(message.chat.id - message.message_id)
        else:
            await tiktok.download_video(message.text, message.chat.id - message.message_id)
            author, descr, shortlink, descr_second = await tiktok.adl(message.text, 'group')
            video = InputFile(f'temp/tiktok_video_{message.chat.id - message.message_id}.mp4')
            await message.answer_video(video, caption=f'👤 {user}\n\n🔗 {shortlink}')
            await message.delete()
            await tiktok.tiktok_del(message.chat.id - message.message_id)
    except Exception as ex:
        await message.answer(f'⚠️ Error: {ex}. Попробуйте еще раз')
        await tiktok.tiktok_del(message.chat.id - message.message_id)

@rate_limit(limit=5)
@dp.message_handler(lambda message: (message.text.startswith('https://www.tiktok.com/') and '/t/' in message.text) or message.text.startswith('https://vt.tiktok') or (message.text.startswith('https://www.tiktok.com/') and 'video' in message.text))
async def tiktok_download(message: types.Message):
    try:
        if await tiktok.check_slide(message.text):
            if await region.baku():
                vide_id = "/".join(urlparse(message.text).path.split("/")[1:])
                tt_kb = await tiktok_id_kb(vide_id, message.chat.id)
                await message.reply(await _('<b>Вы отправили слайд-шоу</b>. Как вы хотите скачать?', locales_dict[message.chat.id]), reply_markup=tt_kb)
            else:
                author, descr, shortlink, audio, descr_second = await tiktok_slide_download(message, message.text, 'private')
                caption = f'👤 {shortlink}\n\n📝 {descr}' if descr != '' else f'👤 {shortlink}'
                await dp.bot.send_audio(chat_id=message.chat.id, audio=audio,
                                        caption=caption,
                                        performer=author, title=descr)
                if descr_second:
                    await message.answer(descr_second)
                await dp.bot.delete_message(message.chat.id, message.message_id)
                await tiktok.tiktok_del(message.chat.id - message.message_id)
        else:
            await tiktok.download_video(message.text, message.chat.id - message.message_id)
            author, descr, shortlink, descr_second = await tiktok.adl(message.text, 'private')
            video = InputFile(f'temp/tiktok_video_{message.chat.id - message.message_id}.mp4')
            await message.answer_video(video, caption=f'👤 {shortlink}\n\n📝 {descr}')
            if descr_second:
                    await message.answer(descr_second)
            await message.delete()
            await tiktok.tiktok_del(message.chat.id - message.message_id)
    except Exception as ex:
        await message.answer(f'⚠️ Error: {ex}. Попробуйте еще раз')
        await tiktok.tiktok_del(message.chat.id - message.message_id)

async def tiktok_slide_download(message, full_link, type):
    author, text, shortlink, descr_second = await tiktok.adl(full_link, type)
    await tiktok.download_photo_music(full_link, message.chat.id - message.message_id)
    album = MediaGroup()
    image_files = [os.path.join('temp/', f) for f in os.listdir('temp/') if f.endswith(
        f'{message.chat.id - message.message_id}.jpg') and f.startswith('tiktok_img')]
    image_files_sorted = sorted(image_files, key=lambda x: int(x.split('_')[2]))
    for i, img in enumerate(image_files_sorted):
        if i % 10 == 0 and i != 0:
            await dp.bot.send_media_group(chat_id=message.chat.id, media=album)
            album = MediaGroup()
        photo = InputFile(img)
        album.attach_photo(photo)
    audio = InputFile(f'temp/tiktok_music_{message.chat.id - message.message_id}.mp3')
    await dp.bot.send_media_group(chat_id=message.chat.id, media=album)
    return author, text, shortlink, audio, descr_second

@dp.callback_query_handler(lambda c: c.data.startswith('tt_photo:'), chat_type=["group", "supergroup"])
async def tt_photo_kb(callback: types.CallbackQuery):
    await dp.bot.edit_message_text(await _('Отправил запрос, ожидайте..', locales_dict[callback.message.chat.id]), callback.message.chat.id, callback.message.message_id)
    user = callback.message.reply_to_message.from_user.get_mention(as_html=True)
    full_link = 'https://vt.tiktok.com/' + callback.data.split(':')[
        1] if '@' not in callback.data else 'https://www.tiktok.com/' + callback.data.split(':')[1]
    author, descr, shortlink, audio, descr_second = await tiktok_slide_download(callback.message, full_link, 'group')
    await dp.bot.send_audio(chat_id=callback.message.chat.id, audio=audio,
                            caption=f'👤 {user}\n\n🔗 {shortlink}',
                            performer=author, title=author)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.reply_to_message.message_id)
    await tiktok.tiktok_del(callback.message.chat.id - callback.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('tt_photo:'))
async def tt_photo_kb(callback: types.CallbackQuery):
    await dp.bot.edit_message_text(await _('Отправил запрос, ожидайте..', locales_dict[callback.message.chat.id]), callback.message.chat.id, callback.message.message_id)
    full_link = 'https://vt.tiktok.com/' + callback.data.split(':')[
        1] if '@' not in callback.data else 'https://www.tiktok.com/' + callback.data.split(':')[1]
    author, descr, shortlink, audio, descr_second = await tiktok_slide_download(callback.message, full_link, 'private')
    caption = f'👤 {shortlink}\n\n📝 {descr}' if descr != '' else f'👤 {shortlink}'
    await dp.bot.send_audio(chat_id=callback.message.chat.id, audio=audio,
                            caption=caption,
                            performer=author, title=descr)
    if descr_second:
        await callback.message.answer(descr_second)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.reply_to_message.message_id)
    await tiktok.tiktok_del(callback.message.chat.id - callback.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('tt_video:'), chat_type=["group", "supergroup"])
async def tt_video_kb(callback: types.CallbackQuery):
    await dp.bot.edit_message_text(await _('<b>Ожидайте.</b> Процесс может занять много времени...', locales_dict[callback.message.chat.id]), callback.message.chat.id, callback.message.message_id)
    full_link = 'https://vt.tiktok.com/' + callback.data.split(':')[
        1] if '@' not in callback.data else 'https://www.tiktok.com/' + callback.data.split(':')[1]
    author, descr, shortlink, descr_second = await tiktok.adl(full_link, 'group')
    user = callback.message.reply_to_message.from_user.get_mention(as_html=True)
    await tiktok.download_photo_music(full_link, callback.message.chat.id - callback.message.message_id)
    await tiktok.slide_to_video(callback.message.chat.id - callback.message.message_id)
    video = InputFile(f'temp/tiktok_video_{callback.message.chat.id - callback.message.message_id}.mp4')
    await dp.bot.send_video(chat_id=callback.message.chat.id, video=video,
                            caption=f'👤 {user}\n\n🔗 {shortlink}')
    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.reply_to_message.message_id)
    await tiktok.tiktok_del(callback.message.chat.id - callback.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('tt_video:'))
async def tt_video_kb(callback: types.CallbackQuery):
    await dp.bot.edit_message_text(await _('<b>Ожидайте.</b> Процесс может занять много времени...', locales_dict[callback.message.chat.id]), callback.message.chat.id, callback.message.message_id)
    full_link = 'https://vt.tiktok.com/' + callback.data.split(':')[
        1] if '@' not in callback.data else 'https://www.tiktok.com/' + callback.data.split(':')[1]
    author, descr, shortlink, descr_second = await tiktok.adl(full_link, 'private')
    await tiktok.download_photo_music(full_link, callback.message.chat.id - callback.message.message_id)
    await tiktok.slide_to_video(callback.message.chat.id - callback.message.message_id)
    video = InputFile(f'temp/tiktok_video_{callback.message.chat.id - callback.message.message_id}.mp4')
    caption = f'👤 {shortlink}\n\n📝 {descr}' if descr != '' else f'👤 {shortlink}'
    await dp.bot.send_video(chat_id=callback.message.chat.id, video=video, parse_mode=None,
                            caption=caption)
    if descr_second:
                    await callback.message.answer(descr_second)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await dp.bot.delete_message(callback.message.chat.id, callback.message.reply_to_message.message_id)
    await tiktok.tiktok_del(callback.message.chat.id - callback.message.message_id)
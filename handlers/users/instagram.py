import os

from aiogram import types
from aiogram.types import InputFile, InputMedia, MediaGroup

from loader import dp
from service import instagram
from utils.misc.throttling import rate_limit


async def download_instagram(message, chat_type):
    link, u_id = message.text, message.chat.id - message.message_id
    descr, shortlink = await instagram.download_initialization(link, u_id)
    album = MediaGroup()
    files = [os.path.join('temp/', f) for f in os.listdir('temp/') if
             (f.endswith(f'{u_id}.jpg') or f.endswith(f'{u_id}.mp4')) and (
                         f.startswith('instagram_photo') or f.startswith('instagram_video'))]
    try:
        files_sorted = sorted(files, key=lambda x: int(x.split('_')[2]))
    except:
        files_sorted = files
        
    user = message.from_user.get_mention(as_html=True)
    if chat_type == 'group':
        caption = f'👤 {user}\n\n🔗 {shortlink}'
    else:
        if descr == '':
            caption = f'👤 {shortlink}'
        else:
            caption = f'👤 {shortlink}\n\n📝 {descr}'
    for i, content in enumerate(files_sorted):
        final_content = InputFile(content)
        if content.endswith(f'{u_id}.mp4'):
            if i == 0:
                album.attach_video(final_content, caption=caption)
            else:
                album.attach_video(final_content)
        else:
            if i == 0:
                album.attach_photo(final_content, caption=caption)
            else:
                album.attach_photo(final_content)
    return album

@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.instagram.com/p/') or message.text.startswith('https://www.instagram.com/reel/'), chat_type=["group", "supergroup"])
async def instagram_group(message: types.Message):
    album = await download_instagram(message, 'group')
    await message.answer_media_group(media=album)
    await message.delete()
    await instagram.instagram_del(message.chat.id - message.message_id)

@rate_limit(limit=5)
@dp.message_handler(lambda message: message.text.startswith('https://www.instagram.com/p/') or message.text.startswith('https://www.instagram.com/reel/'))
async def instagram_private(message: types.Message):
    album = await download_instagram(message, 'private')
    await message.answer_media_group(media=album)
    await message.delete()
    await instagram.instagram_del(message.chat.id - message.message_id)
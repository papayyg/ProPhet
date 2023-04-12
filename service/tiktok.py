import asyncio
import os
import warnings
import requests
from playwright.async_api import async_playwright
import aiohttp
import moviepy.video.fx.all as vfx
import psutil
from bs4 import BeautifulSoup
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
from PIL import Image
import aiofiles


def ignore_moviepy_warning(message, category, filename, lineno, file=None, line=None):
    if category == UserWarning and "FFMPEG" in str(message):
        return None
    else:
        return (message, category, filename, lineno, file, line)


warnings.showwarning = ignore_moviepy_warning

headers = {
    'authority': 'ssstik.io',
    'accept': '*/*',
    'accept-language': 'ru-AZ,ru;q=0.9,en-AZ;q=0.8,en;q=0.7,ru-RU;q=0.6,en-US;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'hx-current-url': 'https://ssstik.io/ru',
    'hx-request': 'true',
    'hx-target': 'target',
    'hx-trigger': '_gcaptcha_pt',
    'origin': 'https://ssstik.io',
    'referer': 'https://ssstik.io/ru',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

params = {
    'url': 'dl',
}

slide_duration = 2


async def slide_to_video(path):
    image_files = [os.path.join(f'temp/', f) for f in os.listdir('temp/') if
                   f.endswith(f'{path}.jpg') and f.startswith('tiktok_')]
    image_slides = []
    for image in image_files:
        slide = VideoFileClip(image).set_duration(slide_duration)
        image_slides.append(slide)
    music_clip = AudioFileClip(f'temp/tiktok_music_{path}.mp3')
    video_clips = []
    if music_clip.duration > 20 > sum([image.duration for image in image_slides]):
        music_clip = music_clip.set_duration(20)
    audio_duration = music_clip.duration
    while sum([clip.duration for clip in video_clips]) < audio_duration:
        for i in image_slides:
            video_clips.extend([i.fx(vfx.fadein, 0.5), i.fx(vfx.fadeout, 0.5)])
            if sum([clip.duration for clip in video_clips]) >= audio_duration:
                break
    video_clip = concatenate_videoclips(video_clips, method="compose")
    video_clip = video_clip.set_audio(music_clip)

    return await asyncio.to_thread(video_clip.write_videofile, f'temp/tiktok_video_{path}.mp4', fps=24, logger=None)


async def check_slide(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            r = await response.text()
            return 1 if '-image.jpeg' in r else 0


async def adl(link, chat_type):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            shortlink = link
            r = await response.text()
            Soup = BeautifulSoup(r, "html.parser")
            author = Soup.select_one('span.e17fzhrb1').text
            shortlink = f'<a href="{shortlink}">{author}</a>'
            if chat_type == 'group': return '', '', shortlink
            descr = ''
            for i in Soup.find_all('span', {'class': 'efbd9f0'}):
                descr += f'{i.text} '
            descr.replace('<', '\\<')
            descr.replace('>', '\\>')
            descr_second = 0
            if len(descr) > 870:
                descr_second = descr[870:]
                descr = descr[:870]
        return author, descr.strip(), shortlink, descr_second


async def download_photo_music(link, path):
    async with aiohttp.ClientSession() as session:
        data = {
            'id': link,
            'locale': 'ru',
            'tt': 'a0RGWTU5',
        }
        async with session.post('https://ssstik.io/abc', params=params, headers=headers, data=data) as response:
            html = await response.text()
            downloadSoup = BeautifulSoup(html, "html.parser")
            music_link = downloadSoup.select_one('a.music')['href']
            async with session.get(music_link) as downloadResponse:
                content = await downloadResponse.read()
                with open(f'temp/tiktok_music_{path}.mp3', "wb") as f:
                    f.write(content)
            for i, img_link in enumerate([img['src'] for img in downloadSoup.find_all('img')[:-1]]):
                async with session.get(img_link) as downloadResponse:
                    content = await downloadResponse.read()
                    with open(f'temp/tiktok_img_{i}_{path}.webp', "wb") as f:
                        f.write(content)
                    with Image.open(f'temp/tiktok_img_{i}_{path}.webp') as im:
                        im.convert('RGB').save(f'temp/tiktok_img_{i}_{path}.jpg', 'JPEG', quality=80)


async def tiktok_del(path):
    for proc in psutil.process_iter():
        try:
            if proc.name() == "ffmpeg-win64-v4.2.2.exe":
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    for file in os.listdir("temp/"):
        if file.startswith("tiktok_") and (
                file.endswith(f"{path}.jpg") or file.endswith(f"{path}.mp3") or file.endswith(
            f"{path}.webp") or file.endswith(f"{path}.mp4")):
            os.remove(os.path.join("temp/", file))


async def download_video(link, path):
    headers = {'referer': 'https://www.tiktok.com/'}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(link)
        await page.wait_for_selector('video')
        video = await page.query_selector('video')
        video_url = await video.get_attribute('src')
        cookies = await page.context.cookies()
        tt_chain_token = None
        for cookie in cookies:
            if cookie['name'] == 'tt_chain_token':
                tt_chain_token = cookie['value']
                break
        await browser.close()
        cookies = {
            'tt_chain_token': tt_chain_token,
        }
        response = await asyncio.to_thread(requests.get, video_url, cookies=cookies, headers=headers)
        async with aiofiles.open(f'temp/tiktok_video_{path}.mp4', 'wb') as f:
            await f.write(response.content)
    # async with aiohttp.ClientSession() as session:
    #     data = {
    #         'id': link,
    #         'locale': 'ru',
    #         'tt': 'a0RGWTU5',
    #     }
    #     async with session.post('https://ssstik.io/abc', params=params, headers=headers, data=data) as response:
    #         html = await response.text()
    #         downloadSoup = BeautifulSoup(html, "html.parser")
    #         downloadLink = downloadSoup.a["href"]
    #         async with session.get(downloadLink) as downloadResponse:
    #             content = await downloadResponse.read()
    #             with open(f'temp/tiktok_video_{path}.mp4', "wb") as f:
    #                 f.write(content)


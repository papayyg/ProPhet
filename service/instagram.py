import asyncio
import os
import re
import urllib.request

from playwright.async_api import async_playwright


async def download_initialization(link, path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(link)
        await page.wait_for_load_state()
        try:
            json_obj = await page.evaluate('''() =>
                {
                    let ldjsonEl = document.querySelector('script[type="application/ld+json"]');
                    return JSON.parse(ldjsonEl.innerHTML);
                }''')
            if json_obj['video'] and json_obj['image']:
                await video_and_photo_download(json_obj['video'], json_obj['image'], path)
            elif json_obj['video']:
                await video_download(json_obj['video'], path)
            elif json_obj['image']:
                await photo_download(json_obj['image'], path)
            descr, shortlink = await adl(json_obj)
        except:
            await page.goto(link)
            video_selector = 'video'
            await page.wait_for_selector(video_selector)

            # найти первый тег video на странице
            video = await page.query_selector(video_selector)

            # получить значение атрибута src
            src = await video.get_attribute('src')
            await except_video(src, path)
            shortlink = f'<a href="{link}">Автор</a>'
            descr, shortlink = '', shortlink
        await browser.close()
        return descr, shortlink
    

async def adl(json_obj):
    descr = json_obj['articleBody']
    descr.replace('<', '\\<')
    descr.replace('>', '\\>')
    author = json_obj['author']['identifier']['value']
    shortlink = re.search(r"https://www\.instagram\.com/(?:p|reel)/\S+/", json_obj['mainEntityOfPage']['@id']).group(0)
    shortlink = f'<a href="{shortlink}">{author}</a>'
    return descr.strip(), shortlink


async def except_video(src, path):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, urllib.request.urlretrieve, src, f'temp/instagram_video_{path}.mp4')
    await future


async def video_and_photo_download(videos, images, path):
    if len(videos) > 1:
        await many_items(videos, 'contentUrl', path)
    else:
        await one_item(videos, 'contentUrl', path)
    if len(images) > 1:
        await many_items(images, 'url', path)
    else:
        await one_item(images, 'url', path)

async def video_download(videos, path):
    if len(videos) > 1:
        await many_items(videos, 'contentUrl', path)
    else:
        await one_item(videos, 'contentUrl', path)

async def photo_download(images, path):
    if len(images) > 1:
        await many_items(images, 'url', path)
    else:
        await one_item(images, 'url', path)

async def one_item(contents, content_type, path):
    content_extensions = 'mp4' if content_type == 'contentUrl' else 'jpg'
    content_name = 'video' if content_type == 'contentUrl' else 'photo'
    content_src = contents[0][content_type]
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, urllib.request.urlretrieve, content_src, f'temp/instagram_{content_name}_{path}.{content_extensions}')
    await future

async def many_items(contents, content_type, path):
    content_extensions = 'mp4' if content_type == 'contentUrl' else 'jpg'
    content_name = 'video' if content_type == 'contentUrl' else 'photo'
    for i, content in enumerate(contents):
        content_src = content[content_type]
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, urllib.request.urlretrieve, content_src, f'temp/instagram_{content_name}_{i}_{path}.{content_extensions}')
        await future

async def instagram_del(path):
    for file in os.listdir("temp/"):
        if file.startswith("instagram_") and (file.endswith(f"{path}.jpg") or file.endswith(f"{path}.mp4")):
            os.remove(os.path.join("temp/", file))
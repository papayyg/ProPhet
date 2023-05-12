import aiohttp

headers = {
    'authority': 'api.ssyoutube.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-AZ,ru;q=0.9,en-AZ;q=0.8,en;q=0.7,ru-RU;q=0.6,en-US;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://ssyoutube.com',
    'referer': 'https://ssyoutube.com/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

async def download_video(link, path):
    json_data = {
        'url': link,
        'ts': 1683893511841,
        '_ts': 1683882187018,
        '_tsc': 0,
        '_s': "5253580d7a839363d93abd57b777629f526d6d6f4c25f7b2bdc77ee0b387dc3a"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.ssyoutube.com/api/convert', headers=headers, json=json_data) as response:
            result = await response.json()
            my_list = result["url"]
            quality_values = ["1080", "720", "480", "360"]
            for quality in quality_values:
                for item in my_list:
                    if isinstance(item, dict) and item.get("quality") == quality and item.get("no_audio") == False:
                        async with session.get(item["url"]) as downloadResponse:
                            content = await downloadResponse.read()
                            with open(f'temp/youtube_video_{path}.mp4', "wb") as f:
                                f.write(content)
                        return
                    else:
                        continue
                else:
                    continue

async def download_audio(link, path):
    json_data = {
        'url': link,
        'ts': 1683721636184,
        '_ts': 1683717844641,
        '_tsc': 0,
        '_s': 'ad552218a89b6a7d3bf16eadfe785024c1e36d39d210a4a13c430290133763c0',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.ssyoutube.com/api/convert', json=json_data) as response:
            result = await response.json()
            for item in reversed(result["url"]):
                if item.get('type') == 'opus audio':
                    async with session.get(item["url"]) as downloadResponse:
                        content = await downloadResponse.read()
                        with open(f'temp/youtube_audio_{path}.mp3', "wb") as f:
                            f.write(content)
                    return
            
            

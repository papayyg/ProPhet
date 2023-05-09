import aiohttp

async def download_video(link, path):
    json_data = {
        'url': link,
        'ts': 1683653670066,
        '_ts': 1683647350473,
        '_tsc': 0,
        '_s': 'de558fe6532a4233ce9b07f659f9d30a5adfd98994848f6dcdcb36411b35155f',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://ssyoutube.com/api/convert', json=json_data) as response:
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
        'ts': 1683653670066,
        '_ts': 1683647350473,
        '_tsc': 0,
        '_s': 'de558fe6532a4233ce9b07f659f9d30a5adfd98994848f6dcdcb36411b35155f',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://ssyoutube.com/api/convert', json=json_data) as response:
            result = await response.json()
            for item in reversed(result["url"]):
                if item.get('type') == 'opus audio':
                    async with session.get(item["url"]) as downloadResponse:
                        content = await downloadResponse.read()
                        with open(f'temp/youtube_audio_{path}.mp3', "wb") as f:
                            f.write(content)
                    return
            
            

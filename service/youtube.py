import aiohttp

async def download_video(link, path):
    json_data = {
        'url': link,
        'ts': 1682633662727,
        '_ts': 1682590840018,
        '_tsc': 0,
        '_s': 'faaeca2fe2fbeabac7186f7a43cb0e297a86c956ea1172e554f3ce7611c1c57f',
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
        'ts': 1682633662727,
        '_ts': 1682590840018,
        '_tsc': 0,
        '_s': 'faaeca2fe2fbeabac7186f7a43cb0e297a86c956ea1172e554f3ce7611c1c57f',
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
            
            

import asyncio
import httpx

headers = {
    'authority': 'api.fabdl.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-AZ,ru;q=0.9,en-AZ;q=0.8,en;q=0.7,ru-RU;q=0.6,en-US;q=0.5',
    'origin': 'https://apple-music-downloader.com',
    'referer': 'https://apple-music-downloader.com/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


async def get_music(url, path):
    params = {
        'url': url,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.fabdl.com/apple-music/get', params=params, headers=headers)
        response_json = response.json()
        gid = response_json["result"]["gid"]
        track_id = response_json["result"]["id"]
        image = response_json["result"]["image"]
        response = await client.get(image)
        with open(f'temp/image_{path}.jpg', 'wb') as file:
            file.write(response.content)
        try:
            link = f'https://api.fabdl.com{response_json["result"]["download_url"]}'
            response = await client.get(link)
            with open(f'temp/apple_{path}.mp3', 'wb') as file:
                file.write(response.content)
            return 1
        except:
            try:
                response = await client.get('https://api.fabdl.com/apple-music/get', params=params, headers=headers)
                response_json = response.json()
                gid = response_json["result"]["gid"]
                track_id = response_json["result"]["id"]
                response = await client.get(f'https://api.fabdl.com/apple-music/mp3-convert-task/{gid}/{track_id}', headers=headers)
                response_json = response.json()
                link = f'https://api.fabdl.com{response_json["result"]["download_url"]}'
                response = await client.get(link)
                with open(f'temp/apple_{path}.mp3', 'wb') as file:
                    file.write(response.content)
                return 1
            except:
                return 0
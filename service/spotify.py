import asyncio
import aiohttp
from data.config import CLIENT_ID, CLIENT_SECRET
from pytube import YouTube

async def get_spotify_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://accounts.spotify.com/api/token', data=data) as response:
            response_json = await response.json()
            return response_json['access_token']

async def get_spotify_track_info(access_token, track_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers) as response:
            response_json = await response.json()
            return response_json

async def download_cover_image(image_url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            image_data = await response.read()
            with open(f'temp/image_{path}.jpg', 'wb') as file:
                file.write(image_data)


async def search_youtube_video(track_title):
    params = {
        'part': 'snippet',
        'q': track_title,
        'maxResults': 1,
        'key': 'AIzaSyD3-3veZRJVwX4RN40XI_2g_FsSr8zcP24',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.googleapis.com/youtube/v3/search', params=params) as response:
            response_json = await response.json()
            video_id = response_json['items'][0]['id']['videoId']
            return video_id
        
async def download_audio(video_id, path):
    youtube_url = f'https://youtu.be/{video_id}'
    yt = YouTube(youtube_url)
    audio = yt.streams.get_audio_only()
    audio_file = f"temp/audio_{path}.mp3"
    audio.download(filename=audio_file)
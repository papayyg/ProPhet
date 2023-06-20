import aiohttp
from pytube import YouTube


async def download_video(link, path):
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    video_filename = f'temp/youtube_video_{path}.mp4'
    video.download(filename=video_filename)

async def download_audio(link, path):
    yt = YouTube(link)
    audio = yt.streams.get_audio_only()
    audio_filename = f"temp/youtube_audio_{path}.mp3"
    audio.download(filename=audio_filename)
            
            

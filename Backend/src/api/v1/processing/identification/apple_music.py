import aiohttp
from fastapi import HTTPException

from Backend.src.api.root.settings import APPLE_MUSIC
from Backend.src.api.v1.db.operations import find_instance


class AppleMusicProviderSearch:
    def __init__(self, db):
        self.db = db

    @property
    def name(self) -> str:
        return APPLE_MUSIC

    async def get_headers(self):
        credentials = await find_instance(db=self.db, provider=self.name)
        headers = {"Authorization": f"Bearer {credentials['access_token']}"}
        return headers

    async def search_by_id(self, song_id: str) -> dict:
        headers = await self.get_headers()
        endpoint = f"https://api.music.apple.com/v1/catalog/us/songs/{song_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException

                data = await response.json()
                return data

    async def search_by_isrc(self, song_isrc: str) -> dict:
        headers = await self.get_headers()
        endpoint = (
            f"https://api.music.apple.com/v1/catalog/us/songs?filter[isrc]={song_isrc}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException

                data = await response.json()
                return data

    async def get_music_video(self, music_video_id) -> dict:
        headers = await self.get_headers()
        endpoint = (
            f"https://api.music.apple.com/v1/catalog/us/music-videos/{music_video_id}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException

                data = await response.json()
                return data

    # ..
    # Parsers
    def parsing_song_by_id(self, data: dict) -> dict:
        track = data["data"][0]
        song_id = track["id"]
        isrc = track["attributes"]["isrc"]
        song_link = track["attributes"]["url"]

        return {"song_id": song_id, "isrc": isrc, "song_link": song_link}

    def parsing_song_by_isrc(self, data: dict) -> dict:
        track = data["data"][0]
        song_id = track["id"]
        isrc = track["attributes"]["isrc"]
        song_link = track["attributes"]["url"]

        return {"song_id": song_id, "isrc": isrc, "song_link": song_link}

    def parsing_music_video(self, data: dict) -> str:
        music_video_url = data["data"][0]["attributes"]["previews"][0]["url"]
        return music_video_url

import aiohttp
from fastapi import HTTPException

from Backend.src.api.root.settings import SPOTIFY
from Backend.src.api.v1.db.operations import find_instance


class SpotifyProviderSearch:
    def __init__(self, db):
        self.db = db

    @property
    def name(self) -> str:
        return SPOTIFY

    async def __get_headers(self):
        credentials = await find_instance(db=self.db, provider=self.name)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {credentials['access_token']}",
        }
        return headers

    async def search_by_id(self, song_id: str) -> dict:
        headers = await self.__get_headers()
        endpoint = f"https://api.spotify.com/v1/tracks/{song_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status)

                data = await response.json()
                return data

    async def search_by_isrc(self, song_isrc: str) -> dict:
        headers = await self.__get_headers()
        endpoint = f"https://api.spotify.com/v1/search?type=track&q=isrc:{song_isrc}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException

                data = await response.json()
                return data

    async def get_artist(self, artist_id) -> dict:
        headers = await self.__get_headers()
        endpoint = f"https://api.spotify.com/v1/artists/{artist_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException

                data = await response.json()
                return data

    # ..
    # Parsers
    def parsing_song_by_id(self, data: dict) -> dict:
        song_id = data["id"]
        isrc = data["external_ids"]["isrc"]
        song_link = data["external_urls"]["spotify"]

        return {
            "song_id": song_id,
            "song_link": song_link,
            "isrc": isrc,
        }

    def parse_all_song_data(self, data: dict) -> dict:
        name = data["name"]
        artists = ", ".join(artist_name["name"] for artist_name in data["artists"])
        artist_id = data["artists"][0]["id"]  # get id the First artist
        preview_song_url = data["preview_url"]
        album_image = data["album"]["images"][0]["url"]
        return {
            "name": name,
            "artists": artists,
            "artist_id": artist_id,
            "preview_song_url": preview_song_url,
            "album_image": album_image,
        }

    def parsing_song_by_isrc(self, data: dict) -> dict:
        track = data["tracks"]["items"][0]
        song_id = track["id"]
        isrc = track["external_ids"]["isrc"]
        song_link = track["external_urls"]["spotify"]

        return {"song_id": song_id, "isrc": isrc, "song_link": song_link}

    def parsing_artist(self, data: dict) -> str:
        return data["images"][0]["url"]

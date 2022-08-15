import urllib
from base64 import b64encode

import aiohttp
from fastapi import HTTPException

from Backend.src.api.root import settings
from Backend.src.api.root.settings import SPOTIFY, APPLE_MUSIC
from Backend.src.api.v1.dataclasses.user import BearerStructure
from Backend.src.api.v1.contrib.utils import calculate_expires_time
from Backend.src.api.v1.db.operations import create_credentials, update_credentials


class SpotifyOAuthClient:
    def __init__(self):
        self.spotify_secret = settings.SPOTIFY_SECRET
        self.spotify_client_id = settings.SPOTIFY_CLIENT_ID
        self.callback_redirect_uri = settings.SPOTIFY_CALLBACK_REDIRECT_URI

    @property
    def get_service_link(self) -> str:
        scopes = [
            "user-read-private",
            "user-read-email",
        ]
        url_scopes = urllib.parse.quote(" ".join(scopes))
        route = (
            f"https://accounts.spotify.com/authorize?response_type=code"
            f"&client_id={self.spotify_client_id}"
            f"&scope={url_scopes}"
            f"&redirect_uri={self.callback_redirect_uri}"
        )

        return route

    async def get_service_tokens(self, code: str) -> dict:
        route = "https://accounts.spotify.com/api/token"
        encode_basic = b64encode(
            ":".join((self.spotify_client_id, self.spotify_secret)).encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {encode_basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {
            "redirect_uri": self.callback_redirect_uri,
            "grant_type": "authorization_code",
            "code": code,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(route, data=payload, headers=headers) as response:
                if response.status != 200:
                    message = (
                        f"Send to endpoint {route} failed! Status: {response.status}"
                    )
                    raise HTTPException(status_code=response.status, detail=message)
                data = await response.json()
                return data

    async def get_profile_data(self, tokens: BearerStructure) -> dict:
        route = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {tokens.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(route, headers=headers) as response:
                if response.status != 200:
                    message = (
                        f"Send to endpoint {route} failed! Status: {response.status}"
                    )
                    raise HTTPException(status_code=response.status, detail=message)
                data = await response.json()
                return data

    async def get_updated_tokens(self, refresh_token: str):
        route = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "refresh_token",
            "code": refresh_token,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(route, data=payload) as response:
                if response.status != 200:
                    message = (
                        f"Send to endpoint {route} failed! Status: {response.status}"
                    )
                    raise HTTPException(status_code=response.status, detail=message)
                data = await response.json()
                return data


class UserAuthController:
    def __init__(self, db):
        self.client = SpotifyOAuthClient()
        self.db = db

    async def create_or_update_credentials(self, code: str) -> None:
        """Method for working with authorization"""

        bearer_tokens = await self.client.get_service_tokens(code=code)
        expires_timestamp = calculate_expires_time(bearer_tokens["expires_in"])
        bearer_tokens.update(
            {"expires_timestamp": expires_timestamp, "provider": SPOTIFY}
        )

        _, created = await create_credentials(
            db=self.db, credential_data=bearer_tokens, provider=SPOTIFY
        )
        if not created:
            _ = await update_credentials(
                db=self.db, credential_data=bearer_tokens, provider=SPOTIFY
            )

    async def create_or_update_am_credentials(self, access_token: str) -> None:
        bearer_tokens = {"access_token": access_token, "provider": APPLE_MUSIC}
        _, created = await create_credentials(
            db=self.db, credential_data=bearer_tokens, provider=APPLE_MUSIC
        )
        if not created:
            _ = await update_credentials(
                db=self.db, credential_data=bearer_tokens, provider=APPLE_MUSIC
            )

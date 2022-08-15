import logging
import functools
import typing
from datetime import datetime
from base64 import b64encode

import aiohttp
from fastapi import HTTPException

from Backend.src.api.root.settings import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET, SPOTIFY
from Backend.src.api.v1.contrib.utils import calculate_expires_time
from Backend.src.api.v1.db.operations import find_instance, update_credentials

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class RecreateServiceTokensSpotify:
    def __init__(self, service_refresh_token: str):
        self.refresh_token = service_refresh_token

    @classmethod
    def __parse_access_token(cls, data: dict) -> str:
        access_token = data["access_token"]
        return access_token

    @classmethod
    def __create_timestamp(cls, data: dict) -> datetime:
        expires_in = data["expires_in"]
        now = datetime.now()
        expires_timestamp = expires_in + datetime.timestamp(now)
        return expires_timestamp

    def formation_data(self, data: dict):
        refreshed_data = {
            "access_token": self.__parse_access_token(data=data),
            "expires_in": self.__create_timestamp(data=data),
        }
        return refreshed_data

    def header_formation(self) -> dict:
        encode_basic = b64encode(
            ":".join((SPOTIFY_CLIENT_ID, SPOTIFY_SECRET)).encode()
        ).decode()
        headers = {"Authorization": f"Basic {encode_basic}"}
        return headers

    def payload_formation(self) -> dict:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        return payload

    async def service_tokens(self) -> dict:
        url = "https://accounts.spotify.com/api/token"
        payload = self.payload_formation()
        headers = self.header_formation()

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=payload, headers=headers) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail="Spotify - Failed to update tokens!",
                    )

                data = await response.json()
                expires_timestamp = calculate_expires_time(data["expires_in"])
                data.update({"expires_timestamp": expires_timestamp})
                return self.formation_data(data)


async def check_timestamps(db, spotify_credentials: dict) -> typing.Any or None:
    # TODO: spotify developer data instead self.something
    now = datetime.now()
    service_timestamp = spotify_credentials["expires_timestamp"]
    datetime_service_expired = datetime.fromtimestamp(service_timestamp)

    if datetime_service_expired < now:
        message = f"Spotify Token expired! Recreate"
        logger.warning(message)
        recreate = RecreateServiceTokensSpotify(
            service_refresh_token=spotify_credentials["refresh_token"]
        )
        data = await recreate.service_tokens()
        credentials = await update_credentials(
            db=db, credential_data=data, provider=SPOTIFY
        )
        return credentials
    return


def check_expiration(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        request = kwargs["request"]
        db = request.app.db
        credentials = await find_instance(db=db, provider=SPOTIFY)
        await check_timestamps(db=db, spotify_credentials=credentials)
        response = await func(*args, **kwargs)

        return response

    return inner

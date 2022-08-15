import typing

from fastapi import APIRouter, Request

from Backend.src.api.root.settings import APPLE_MUSIC
from Backend.src.api.v1.auth.spotify import SpotifyOAuthClient, UserAuthController
from Backend.src.api.v1.dataclasses.user import AppleMusicDeveloperBearerStructure
from Backend.src.api.v1.db.operations import find_instance

router = APIRouter()


@router.get("/spotify/callback")
async def spotify_callback(code: str, request: Request) -> typing.Dict:
    db = request.app.db
    controller = UserAuthController(db=db)
    _ = await controller.create_or_update_credentials(code=code)

    return {"message": "success"}


@router.get("/get/spotify/authorized/link")
async def login() -> typing.Dict:
    """
    Service name:
    ----
    * Spotify
    """
    return {"link": SpotifyOAuthClient().get_service_link}


@router.post("/apple/music/tokens")
async def apple_music_upload_developer_token(
    bearer: AppleMusicDeveloperBearerStructure, request: Request
) -> typing.Dict:
    db = request.app.db
    controller = UserAuthController(db=db)
    _ = await controller.create_or_update_am_credentials(
        access_token=bearer.access_token
    )

    return {"message": "success"}

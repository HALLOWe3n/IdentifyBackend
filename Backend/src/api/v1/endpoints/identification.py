from fastapi import APIRouter, Request, Depends

from Backend.src.api.v1.processing.auth.service_expiriations import check_expiration
from Backend.src.api.v1.processing.identification.processing import Processing
from Backend.src.api.v1.auth.auth import OAuth
from Backend.src.api.v1.dataclasses.client import (
    ClientAsksIdentificationModel,
    ClientResponseIdentificationModel,
)

router = APIRouter()


@router.post("/process")
@check_expiration
async def identification_process(
    request: Request,
    client_info: ClientAsksIdentificationModel,
    # user: dict = Depends(OAuth().get_user)
) -> ClientResponseIdentificationModel:
    db = request.app.db
    process = Processing(
        db=db,
        song_id=client_info.songID,
        user_requested_provider=client_info.forProvider,
        song_provider=client_info.fromProvider,
    )
    return await process.identification()


@router.get("/music/video")
async def get_music_video() -> dict:
    return {
        "videoURL": "https://video-ssl.itunes.apple.com/itunes-assets/"
        "Video128/v4/ad/90/c4/ad90c4c9-298f-8970-6bfe-da4c429b85cc/"
        "mzvf_4290135147244435966.720w.h264lc.U.p.m4v"
    }

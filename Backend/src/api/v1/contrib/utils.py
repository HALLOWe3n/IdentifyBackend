from datetime import datetime

from Backend.src.api.root.settings import EXPIRED_TIME_ACCESS_TOKEN


def calculate_expires() -> int:
    return EXPIRED_TIME_ACCESS_TOKEN * 60


def calculate_expires_time(expires_in: int) -> datetime.timestamp:
    now = datetime.now()
    expires_access_token = expires_in + datetime.timestamp(now)
    return expires_access_token

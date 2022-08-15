import typing

from pydantic import BaseModel


class UserStructure(BaseModel):
    user_uuid: str


class BearerStructure(BaseModel):
    access_token: typing.Optional[str] = None
    refresh_token: typing.Optional[str] = None


class AppleMusicDeveloperBearerStructure(BaseModel):
    access_token: str

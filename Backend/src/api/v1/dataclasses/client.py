import typing

from pydantic import BaseModel

# ..
# Base Models for working with iOS client
# Request and Response Models


class ClientAsksIdentificationModel(BaseModel):
    forProvider: str
    fromProvider: str
    songID: str


class BaseIdentificationModel(BaseModel):
    songID: str
    isrc: str
    url: str
    isUserProvider: bool


class IdentificationModel(BaseModel):
    name: str
    data: BaseIdentificationModel


class SongInformationModel(BaseModel):
    name: str
    artists: str
    countIdentification: typing.Optional[str]
    artistImage: str
    albumImage: str
    songURL: typing.Optional[str]
    musicVideoURL: typing.Optional[str]


class ClientResponseIdentificationModel(BaseModel):
    identification: typing.List[IdentificationModel]
    songInformation: SongInformationModel

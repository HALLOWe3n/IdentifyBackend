from typing import Optional
from bson import ObjectId

from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CredentialModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    expires_timestamp: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "ey...",
                "refresh_token": "ey...",
                "expires_timestamp": "1660087309.878153",
            }
        }


class UpdateCredentialModel(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    expires_timestamp: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "ey...",
                "refresh_token": "ey...",
                "expires_timestamp": "1660087309.878153",
            }
        }

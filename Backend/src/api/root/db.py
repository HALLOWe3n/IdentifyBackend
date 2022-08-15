import typing
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from . import settings


def create_mongo_engine():
    uri = f"mongodb://{settings.MONGO_INITDB_ROOT_USERNAME}:{settings.MONGO_INITDB_ROOT_PASSWORD}@{settings.MONGO_SERVER}:{settings.MONGO_PORT}/{settings.MONGO_INITDB_DATABASE}?authSource=admin"
    client = AsyncIOMotorClient(uri)

    db = client.get_database(settings.MONGO_INITDB_DATABASE)
    return db

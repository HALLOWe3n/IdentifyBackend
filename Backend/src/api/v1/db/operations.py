import logging

from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


async def create_credentials(db, credential_data: dict, provider: str):
    credentials = jsonable_encoder(credential_data)

    is_create = False
    instance = await db.credentials.find_one({"provider": provider})

    if not instance:
        is_create = True
        instance = await db.credentials.insert_one(credentials)

    return instance, is_create


async def update_credentials(db, credential_data: dict, provider: str):
    credentials = jsonable_encoder(credential_data)
    instance = await db.credentials.update_one(
        {"provider": provider}, {"$set": credentials}
    )
    return instance


async def find_instance(db, provider: str):
    instance = await db.credentials.find_one({"provider": provider})
    return instance

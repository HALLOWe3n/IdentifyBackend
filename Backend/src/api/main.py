import uvicorn

from fastapi import FastAPI

from Backend.src.api.root.db import create_mongo_engine
from Backend.src.api.v1.endpoints.identification import router as identification_router
from Backend.src.api.v1.endpoints.developers import router as develop_credentials_router


API_V1 = "/api/v1"
app = FastAPI(
    title="Identify backend",
    version="0.0.1",
)

app.include_router(
    router=identification_router, prefix=f"{API_V1}/identify", tags=["Identify"]
)
app.include_router(
    router=develop_credentials_router,
    prefix=f"{API_V1}/develop",
    tags=["develop_credentials_router"],
)


@app.on_event("startup")
async def startup() -> None:
    app.db = create_mongo_engine()

import uvicorn
import uuid
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from api.videos.endpoints.routers import router as videos_router
from api.videos.auth.auth_helper import invoke_api, api_keys

# importing server settings
from api.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "hello"}


@app.get("/api-key")
def get_new_key():
    key = uuid.uuid4().hex

    api_keys[key] = {"status": settings.ACTIVE, "invoke_count": 0}

    return {"key": key}


# initialising motor client on server startup
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    add_pagination(app)


@app.on_event("shutdown")
async def shutdown_db_client():

    app.mongodb_client.close()


app.include_router(
    videos_router, tags=["videos"], prefix="/video", dependencies=[Depends(invoke_api)]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

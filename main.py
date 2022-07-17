import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.videos.routers import router as videos_router

# importing server settings
from config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "hello"}


# initialising motor client on server startup
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]

    # triggering function on startup to add entries to DB
    # await insert_in_db()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(videos_router, tags=["videos"], prefix="/video")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

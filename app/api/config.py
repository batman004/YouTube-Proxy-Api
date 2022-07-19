from fastapi import APIRouter
from pydantic import BaseSettings
from dotenv import dotenv_values

config = dotenv_values(".env")


class CommonSettings(BaseSettings):
    APP_NAME: str = "youtubeFetch"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = config["DB_URL"]
    DB_NAME: str = config["DB_NAME"]


class ApiKeySettings(BaseSettings):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"
    THRESHOLD: int = 5


class YouTubeApiSettings(BaseSettings):
    YOUTUBE_API_TOKEN = config["API_KEY"]


class Settings(
    CommonSettings, ServerSettings, DatabaseSettings, YouTubeApiSettings, ApiKeySettings
):
    pass


settings = Settings()

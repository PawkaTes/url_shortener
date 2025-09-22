import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "DATABASE_URL"
    DEBUG: bool = "DEBUG"

    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCSESS_TOOKEN_EXPIRE_MINUTES: int = 60*24

    PROJECT_NAME: str = "URL Shortener"

    class Config:
        env_file = ".env"

settings = Settings()
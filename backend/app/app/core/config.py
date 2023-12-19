import os
from typing import Any
from enum import Enum

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, field_validator, FieldValidationInfo


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    ASYNC_DATABASE_URI: PostgresDsn | str = ""

    @field_validator("ASYNC_DATABASE_URI", mode="after")
    def assemble_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                return PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=info.data["DATABASE_USER"],
                    password=info.data["DATABASE_PASSWORD"],
                    host=info.data["DATABASE_HOST"],
                    port=info.data["DATABASE_PORT"],
                    path=info.data["DATABASE_NAME"],
                )
        return v

    REDIS_HOST: str
    REDIS_PORT: str

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()

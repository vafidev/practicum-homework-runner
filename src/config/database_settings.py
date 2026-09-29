from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DatabaseSettings(BaseSettings):
    """Database settings for the application"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="DATABASE_",
        case_sensitive=False,
    )

    user: str = Field(min_length=1, max_length=50)
    password: SecretStr = Field(min_length=1)
    host: str = Field(default="localhost")
    port: int = Field(default=5432, ge=1, le=65535)
    db: str = Field(min_length=1)

    echo: bool = Field(default=False)

    pool_size: int = Field(default=10, ge=1, le=100)
    max_overflow: int = Field(default=10, ge=1, le=100)
    pool_timeout: int = Field(default=30, ge=1, le=300)
    recycle: int = Field(default=1800, ge=1, le=3600)
    pool_pre_ping: bool = Field(default=True)
    connect_timeout: int = Field(default=10, ge=2, le=60)

    @property
    def url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        ).render_as_string(hide_password=False)


@lru_cache(maxsize=1)
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()

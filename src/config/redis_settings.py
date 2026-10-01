from functools import lru_cache

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_",
        case_sensitive=False,
    )

    url: RedisDsn

    max_connections: int = Field(default=50, ge=1, le=100)
    socket_connection_timeout: float | int = Field(default=5.0, ge=0.1, le=60.0)
    socket_timeout: float | int = Field(default=5.0, ge=0.1, le=60.0)
    health_check_interval: int = Field(default=30, ge=0, le=600)
    retry_on_timeout: bool = Field(default=True)
    decode_responses: bool = Field(default=True)


@lru_cache(maxsize=1)
def get_redis_settings() -> RedisSettings:
    return RedisSettings()

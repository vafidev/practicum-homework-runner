from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ArgonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="ARGON_",
    )

    memory_cost: int = Field(default=65536, ge=8129, le=1048576)
    time_cost: int = Field(default=3, ge=1, le=10)
    parallelism: int = Field(default=4, ge=1, le=16)
    hash_len: int = Field(default=36, ge=16, le=64)
    salt_len: int = Field(default=16, ge=8, le=32)


@lru_cache(maxsize=1)
def get_argon_settings() -> ArgonSettings:
    return ArgonSettings()

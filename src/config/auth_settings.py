from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="AUTH_",
    )

    jwt_secret_key: SecretStr
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expires_minutes: int = Field(default=15, ge=1, le=60)
    jwt_refresh_token_expires_days: int = Field(default=30, ge=1, le=180)

    cookie_secure: bool = Field(default=True)
    cookie_samesite: Literal["lax", "strict", "none"] = Field(default="lax")
    cookie_domain: str | None = Field(default=None)


@lru_cache(maxsize=1)
def get_auth_settings() -> AuthSettings:
    return AuthSettings()

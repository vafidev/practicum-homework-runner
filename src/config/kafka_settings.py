from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="KAFKA_",
        case_sensitive=False,
    )

    broker_url: str = Field(default="kafka:29092")


@lru_cache(maxsize=1)
def get_kafka_settings() -> KafkaSettings:
    return KafkaSettings()

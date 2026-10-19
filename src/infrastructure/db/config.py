from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.database_settings import get_db_settings
from src.infrastructure.log.logger import logger


class DataBaseConfig:
    def __init__(self) -> None:
        self._settings = get_db_settings()
        self._engine: AsyncEngine | None = None
        self._session: async_sessionmaker[AsyncSession] | None = None

    @property
    def async_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(
                url=self._settings.url,
                echo=self._settings.echo,
                pool_size=self._settings.pool_size,
                max_overflow=self._settings.max_overflow,
                pool_timeout=self._settings.pool_timeout,
                pool_recycle=self._settings.recycle,
                pool_pre_ping=self._settings.pool_pre_ping,
                connect_args={"timeout": self._settings.connect_timeout},
            )
        return self._engine

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        if self._session is None:
            self._session = async_sessionmaker(
                bind=self.async_engine,
                expire_on_commit=False,
                autoflush=False,
            )
        return self._session

    async def disconnect(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session = None
            logger.info("Database disconnected")

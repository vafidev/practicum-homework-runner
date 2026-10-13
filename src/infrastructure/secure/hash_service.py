import asyncio

from argon2 import PasswordHasher, Type
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from config.argon_settings import get_argon_settings
from infrastructure.log.logger import logger


class ArgonService:
    def __init__(self) -> None:
        self._settings = get_argon_settings()
        self._password_hasher = PasswordHasher(
            time_cost=self._settings.time_cost,
            memory_cost=self._settings.memory_cost,
            parallelism=self._settings.parallelism,
            hash_len=self._settings.hash_len,
            salt_len=self._settings.salt_len,
            type=Type.ID,
        )

    @property
    def password_hasher(self) -> PasswordHasher:
        return self._password_hasher

    def _check_password(self, password: str, hashed_password: str) -> bool:
        try:
            result = self.password_hasher.verify(hashed_password, password)
        except VerifyMismatchError:
            logger.warning("Password verification failed")
            return False
        except InvalidHashError:
            logger.error("Stored password hash is malformed")
            raise
        return result

    async def hash_password(self, password: str) -> str:
        return await asyncio.to_thread(self.password_hasher.hash, password)

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return await asyncio.to_thread(self._check_password, password, hashed_password)

    def _verify_and_rehash_sync(
        self, password: str, hashed_password: str
    ) -> tuple[bool, str | None]:
        if not self._check_password(password, hashed_password):
            return False, None
        if self.password_hasher.check_needs_rehash(hashed_password):
            return True, self.password_hasher.hash(password)
        return True, None

    async def verify_and_rehash(
        self, password: str, hashed_password: str
    ) -> tuple[bool, str | None]:
        return await asyncio.to_thread(self._verify_and_rehash_sync, password, hashed_password)

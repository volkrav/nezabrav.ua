from functools import cached_property, lru_cache
from typing import Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    BLACKBOX_API: str
    BLACKBOX_URL: str
    NOVAPOSHTA_API_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @computed_field
    @cached_property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://' +\
            f'{self.DB_USER}:{self.DB_PASS}' +\
            '@' +\
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @computed_field
    @cached_property
    def TEST_DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://' +\
            f'{self.TEST_DB_USER}:{self.TEST_DB_PASS}' +\
            '@' +\
            f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

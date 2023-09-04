from functools import cached_property, lru_cache

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BLACKBOX_API: str
    BLACKBOX_URL: str

    @computed_field
    @cached_property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://' +\
            f'{self.DB_USER}:{self.DB_PASS}' +\
            '@' +\
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #
    MODE: Literal["DEV", "TEST", "PROD"]

    # Postgresql
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    # Test Postgresql
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    @property
    def test_db_url(self):
        return (f'postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}'
                f'/{self.TEST_DB_NAME}')

    # jwt_token
    JWT_KEY: str
    ALGORITHM: str
    JWT_EXPIRE: int
    REFR_EXPIRE: int

    # Redis
    REDIS_PORT: int
    REDIS_HOST: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'MedScheduler'
    ENVIRONMENT: str = 'development'
    DEBUG: bool = True

    DATABASE_URL: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/medscheduler'
    )
    REDIS_URL: str = 'redis://localhost:6379/0'

    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    TELEGRAM_WEBHOOK_SECRET: Optional[str] = None

    TIMEZONE: str = 'America/Sao_Paulo'

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )


settings = Settings()

"""Application configuration"""

import os
from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/taskflow"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS - stored as string, parsed in property
    _ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        if isinstance(self._ALLOWED_ORIGINS, list):
            return self._ALLOWED_ORIGINS
        return [origin.strip() for origin in self._ALLOWED_ORIGINS.split(",")]

    # Email
    EMAIL_PROVIDER: Literal["resend", "sendgrid"] = "resend"
    RESEND_API_KEY: str | None = None
    SENDGRID_API_KEY: str | None = None
    EMAIL_FROM: str = "noreply@taskflow.com"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()

"""Application settings and configuration."""

import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application settings
    APP_TITLE: str = "RAG-Sec Standalone API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Zero-trust runtime safety framework bridging autonomous AI agent reasoning "
        "with secure data infrastructure execution"
    )
    DEBUG: bool = False

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: List[str] = ["*"]

    # Database settings - PostgreSQL (primary)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "ragsec_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False

    @property
    def DATABASE_URL(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # SQLite settings (sandbox deception)
    SQLITE_DB_PATH: str = "sandbox.db"

    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TTL_SECONDS: int = 30  # Token validity window

    # HSM/Cryptography settings
    HSM_KEY_ROTATION_MINUTES: int = 5
    ENABLE_HSM_SIMULATION: bool = True

    # Feature flags
    ENABLE_HONEY_TABLE_DETECTION: bool = True
    ENABLE_DECEPTION_ROUTING: bool = True
    ENABLE_REQUEST_LOGGING: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

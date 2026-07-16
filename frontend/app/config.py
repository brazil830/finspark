"""
Configuration management for RAG-Sec Standalone backend.

Uses pydantic-settings to load environment variables with validation.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/rag_sec"
    sandbox_database_url: str = "sqlite:///./sandbox.db"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Security & Cryptography
    secret_key: str = "change-me-in-production-use-strong-random-key"
    hsm_key_rotation_minutes: int = 5
    token_expiry_seconds: int = 30
    
    # CORS & Frontend
    frontend_origin: str = "http://localhost:5173"
    
    # Logging
    log_level: str = "INFO"
    
    # Database Pool
    db_pool_size: int = 20
    db_max_overflow: int = 10
    
    class Config:
        """Pydantic config for settings."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

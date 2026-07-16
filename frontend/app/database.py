"""
Database connection and session management.

Provides async SQLAlchemy engine and session factory for PostgreSQL.
"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and session lifecycle."""
    
    def __init__(self):
        """Initialize database manager with connection pool."""
        self.engine = None
        self.session_factory = None
    
    async def initialize(self) -> None:
        """Initialize the database engine and session factory."""
        logger.info(f"Initializing database connection to {settings.database_url}")
        
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            poolclass=NullPool if settings.debug else None,
        )
        
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        logger.info("Database engine initialized successfully")
    
    async def close(self) -> None:
        """Close the database engine."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database engine closed")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session."""
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        session = self.session_factory()
        try:
            yield session
        finally:
            await session.close()


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection for database sessions."""
    async for session in db_manager.get_session():
        yield session

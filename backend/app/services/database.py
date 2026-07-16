"""Database connection and initialization services."""

import logging
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from database.engine import (
    PostgresSessionFactory,
    SQLiteSessionFactory,
    pg_engine,
    sqlite_engine,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections for PostgreSQL and SQLite."""

    def __init__(self):
        """Initialize database manager."""
        self.pg_engine: Optional[AsyncEngine] = pg_engine
        self.sqlite_engine: Optional[AsyncEngine] = sqlite_engine
        self._session: Optional[AsyncSession] = None

    async def initialize(self, database_url: str, sqlite_path: str):
        """Initialize database connections.

        Args:
            database_url: PostgreSQL connection URL
            sqlite_path: Path to SQLite database file
        """
        # Initialize PostgreSQL connection if available
        if self.pg_engine is not None and PostgresSessionFactory is not None:
            try:
                logger.info(f"Testing PostgreSQL connection: {database_url}")
                async with self.pg_engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("PostgreSQL connection successful")
            except Exception as e:
                logger.warning(
                    f"PostgreSQL connection unavailable: {e}. "
                    "Routes will use fallback mock data."
                )
                self.pg_engine = None
        else:
            logger.warning(
                "PostgreSQL engine not configured. Routes will use fallback mock data."
            )

        # Initialize SQLite connection for sandbox
        if self.sqlite_engine is not None and SQLiteSessionFactory is not None:
            try:
                logger.info("Testing SQLite sandbox connection")
                async with self.sqlite_engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("SQLite sandbox connection successful")
            except Exception as e:
                logger.error(f"SQLite sandbox connection failed: {e}")
                raise
        else:
            raise RuntimeError("SQLite sandbox engine is required")

    async def close(self):
        """Close all database connections."""
        try:
            if self.pg_engine:
                await self.pg_engine.dispose()
                logger.info("PostgreSQL connection closed")

            if self.sqlite_engine:
                await self.sqlite_engine.dispose()
                logger.info("SQLite connection closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

    async def get_pg_session(self) -> AsyncSession:
        """Get PostgreSQL async session."""
        if not self.pg_engine or PostgresSessionFactory is None:
            raise RuntimeError("PostgreSQL engine not initialized")
        return PostgresSessionFactory()


# Global database manager instance
_db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    return _db_manager

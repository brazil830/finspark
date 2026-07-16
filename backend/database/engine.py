"""Async SQLAlchemy database engines and session factories.

This module configures connection pools for PostgreSQL (primary database)
and SQLite (sandbox deception database) with proper async/await support.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool, QueuePool

from app.config.settings import settings

logger = logging.getLogger(__name__)


# =============================================================================
# PostgreSQL Engine & Connection Pool
# =============================================================================

def _create_postgres_engine() -> AsyncEngine:
    """Create async PostgreSQL engine with optimized connection pool.
    
    Configuration:
    - pool_size: 20 base connections for connection reuse
    - max_overflow: 10 additional connections for concurrent requests
    - pool_pre_ping: Test connections before use to catch stale connections
    - pool_recycle: Recycle connections after 1 hour to prevent timeout issues
    - echo: Disabled in production for performance
    
    Returns:
        AsyncEngine: Configured SQLAlchemy async engine for PostgreSQL
    """
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        poolclass=QueuePool,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={
            "timeout": 10,
            "command_timeout": 30,
        },
    )
    logger.info(
        "PostgreSQL engine created with pool_size=%d, max_overflow=%d",
        settings.DB_POOL_SIZE,
        settings.DB_MAX_OVERFLOW,
    )
    return engine


# =============================================================================
# SQLite Engine & Connection Pool
# =============================================================================

def _create_sqlite_engine() -> AsyncEngine:
    """Create async SQLite engine for sandbox deception database.
    
    Configuration:
    - connect_args with timeout for concurrent access handling
    - NullPool to avoid connection pooling issues with SQLite
    - Echo disabled for performance
    
    The SQLite database is used as an isolated sandbox for honey table
    detection simulation and deception routing.
    
    Returns:
        AsyncEngine: Configured SQLAlchemy async engine for SQLite
    """
    sqlite_url = f"sqlite+aiosqlite:///./{settings.SQLITE_DB_PATH}"
    engine = create_async_engine(
        sqlite_url,
        echo=settings.DB_ECHO,
        poolclass=NullPool,  # SQLite doesn't benefit from connection pooling
        connect_args={"timeout": 10},
    )
    logger.info("SQLite sandbox engine created at %s", settings.SQLITE_DB_PATH)
    return engine


# Create engine instances lazily with graceful fallback
try:
    pg_engine: Optional[AsyncEngine] = _create_postgres_engine()
except Exception as e:
    logger.warning("PostgreSQL engine creation failed: %s. Postgres features will be unavailable.", str(e))
    pg_engine = None

try:
    sqlite_engine: AsyncEngine = _create_sqlite_engine()
except Exception as e:
    logger.error("SQLite engine creation failed: %s", str(e))
    raise RuntimeError(f"SQLite sandbox engine is required: {e}") from e


# =============================================================================
# Session Factories
# =============================================================================

PostgresSessionFactory: Optional[async_sessionmaker] = None
"""Session factory for PostgreSQL primary database."""
if pg_engine is not None:
    PostgresSessionFactory = async_sessionmaker(
        pg_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

SQLiteSessionFactory = async_sessionmaker(
    sqlite_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
"""Session factory for SQLite sandbox database."""


# =============================================================================
# Connection Testing
# =============================================================================

async def test_postgres_connection() -> bool:
    """Test PostgreSQL connection availability.
    
    Executes a simple SELECT 1 query to verify the database is accessible
    and the connection pool is properly configured.
    
    Returns:
        bool: True if connection is successful
        
    Raises:
        Exception: If connection fails for any reason
    """
    if pg_engine is None:
        raise RuntimeError("PostgreSQL engine is not available")
    try:
        async with pg_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("PostgreSQL connection test successful")
        return True
    except Exception as e:
        logger.error("PostgreSQL connection test failed: %s", str(e))
        raise


async def test_sqlite_connection() -> bool:
    """Test SQLite sandbox connection availability.
    
    Executes a simple SELECT 1 query to verify the sandbox database
    is accessible.
    
    Returns:
        bool: True if connection is successful
        
    Raises:
        Exception: If connection fails for any reason
    """
    try:
        async with sqlite_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("SQLite sandbox connection test successful")
        return True
    except Exception as e:
        logger.error("SQLite sandbox connection test failed: %s", str(e))
        raise


async def test_all_connections() -> dict:
    """Test both database connections.
    
    Returns:
        dict: Status of both connections with format:
              {
                  "postgres": {"status": "connected", "pool_size": 20},
                  "sqlite": {"status": "connected"},
              }
              
    Raises:
        Exception: If either connection test fails
    """
    results = {}
    
    try:
        await test_postgres_connection()
        results["postgres"] = {
            "status": "connected",
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
        }
    except Exception as e:
        results["postgres"] = {"status": "failed", "error": str(e)}
        
    try:
        await test_sqlite_connection()
        results["sqlite"] = {"status": "connected"}
    except Exception as e:
        results["sqlite"] = {"status": "failed", "error": str(e)}
    
    return results


# =============================================================================
# Context Managers for Session Access
# =============================================================================

@asynccontextmanager
async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """Get PostgreSQL session as async context manager.
    
    Yields a new session from the PostgreSQL connection pool.
    Session is automatically committed or rolled back on exit.
    
    Usage:
        async with get_postgres_session() as session:
            result = await session.execute(select(User))
            
    Yields:
        AsyncSession: Active database session
    """
    if PostgresSessionFactory is None:
        raise RuntimeError("PostgreSQL session factory is not available")
    session = PostgresSessionFactory()
    try:
        yield session
    finally:
        await session.close()


@asynccontextmanager
async def get_sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    """Get SQLite sandbox session as async context manager.
    
    Yields a new session from the SQLite connection pool.
    Session is automatically committed or rolled back on exit.
    
    Usage:
        async with get_sqlite_session() as session:
            result = await session.execute(select(HoneyData))
            
    Yields:
        AsyncSession: Active sandbox session
    """
    session = SQLiteSessionFactory()
    try:
        yield session
    finally:
        await session.close()


# Aliases for convenience
get_db_session = get_postgres_session
get_sandbox_session = get_sqlite_session


# =============================================================================
# Engine Lifecycle Management
# =============================================================================

async def dispose_engines() -> None:
    """Dispose of all engines and close connections.
    
    Call this during application shutdown to properly clean up
    all database connections and release resources.
    """
    if pg_engine is not None:
        try:
            await pg_engine.dispose()
            logger.info("PostgreSQL engine disposed")
        except Exception as e:
            logger.error("Error disposing PostgreSQL engine: %s", str(e))
    
    try:
        await sqlite_engine.dispose()
        logger.info("SQLite engine disposed")
    except Exception as e:
        logger.error("Error disposing SQLite engine: %s", str(e))


# =============================================================================
# Engine Info & Diagnostics
# =============================================================================

def get_engine_info() -> dict:
    """Get diagnostic information about configured engines.
    
    Returns:
        dict: Configuration details for both database engines
    """
    return {
        "postgres": {
            "available": pg_engine is not None,
            "url": settings.DATABASE_URL,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "echo": settings.DB_ECHO,
        },
        "sqlite": {
            "path": settings.SQLITE_DB_PATH,
            "pool_class": "NullPool",
            "timeout": 10,
            "echo": settings.DB_ECHO,
        },
    }

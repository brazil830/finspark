"""Tests for async SQLAlchemy database engines and connection pooling.

Tests verify:
- PostgreSQL engine creation and configuration
- SQLite engine creation and configuration  
- Session factory setup and proper cleanup
- Connection pool settings validation
- Engine info and diagnostics
"""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import (
    PostgresSessionFactory,
    SQLiteSessionFactory,
    dispose_engines,
    get_engine_info,
    get_postgres_session,
    get_sandbox_session,
    get_sqlite_session,
    pg_engine,
    sqlite_engine,
    test_all_connections,
    test_postgres_connection,
    test_sqlite_connection,
)


class TestPostgresEngine:
    """Test PostgreSQL engine configuration."""

    def test_postgres_engine_created(self):
        """Verify PostgreSQL engine is properly instantiated."""
        assert pg_engine is not None
        assert pg_engine.url.drivername == "postgresql+asyncpg"

    def test_postgres_engine_pool_config(self):
        """Verify PostgreSQL connection pool settings."""
        pool = pg_engine.pool
        assert pool is not None
        # Pool configuration is set during engine creation

    @pytest.mark.asyncio
    async def test_postgres_connection_test(self):
        """Test PostgreSQL connection availability."""
        result = await test_postgres_connection()
        assert result is True

    @pytest.mark.asyncio
    async def test_postgres_session_factory(self):
        """Verify PostgreSQL session factory creates valid sessions."""
        async with PostgresSessionFactory() as session:
            assert isinstance(session, AsyncSession)
            # Verify we can execute a simple query
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1


class TestSQLiteEngine:
    """Test SQLite engine configuration."""

    def test_sqlite_engine_created(self):
        """Verify SQLite engine is properly instantiated."""
        assert sqlite_engine is not None
        assert "aiosqlite" in sqlite_engine.url.drivername

    @pytest.mark.asyncio
    async def test_sqlite_connection_test(self):
        """Test SQLite sandbox connection availability."""
        result = await test_sqlite_connection()
        assert result is True

    @pytest.mark.asyncio
    async def test_sqlite_session_factory(self):
        """Verify SQLite session factory creates valid sessions."""
        async with SQLiteSessionFactory() as session:
            assert isinstance(session, AsyncSession)
            # Verify we can execute a simple query
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1


class TestSessionContextManagers:
    """Test async context managers for session access."""

    @pytest.mark.asyncio
    async def test_get_postgres_session_context_manager(self):
        """Verify get_postgres_session context manager works correctly."""
        async with get_postgres_session() as session:
            assert isinstance(session, AsyncSession)
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1

    @pytest.mark.asyncio
    async def test_get_sqlite_session_context_manager(self):
        """Verify get_sqlite_session context manager works correctly."""
        async with get_sqlite_session() as session:
            assert isinstance(session, AsyncSession)
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1

    @pytest.mark.asyncio
    async def test_get_sandbox_session_alias(self):
        """Verify get_sandbox_session is proper alias for SQLite."""
        async with get_sandbox_session() as session:
            assert isinstance(session, AsyncSession)
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1


class TestConnectionPooling:
    """Test connection pool behavior and management."""

    @pytest.mark.asyncio
    async def test_concurrent_sessions(self):
        """Test multiple concurrent sessions from pool."""
        sessions = []
        try:
            # Create multiple sessions concurrently
            for _ in range(5):
                session = PostgresSessionFactory()
                sessions.append(session)
                result = await session.execute(text("SELECT 1"))
                assert result.scalar() == 1
        finally:
            # Clean up all sessions
            for session in sessions:
                await session.close()

    @pytest.mark.asyncio
    async def test_session_cleanup_on_exception(self):
        """Verify session cleanup when exception occurs."""
        try:
            async with get_postgres_session() as session:
                # Session should be properly closed even if exception occurs
                raise ValueError("Test exception")
        except ValueError:
            pass
        # If we get here without hanging, cleanup worked

    @pytest.mark.asyncio
    async def test_session_isolation(self):
        """Verify sessions are isolated from each other."""
        async with get_postgres_session() as session1:
            async with get_postgres_session() as session2:
                # Both sessions should be separate instances
                assert session1 is not session2


class TestConnectionDiagnostics:
    """Test connection diagnostics and information retrieval."""

    @pytest.mark.asyncio
    async def test_all_connections(self):
        """Test comprehensive connection status check."""
        status = await test_all_connections()
        assert "postgres" in status
        assert "sqlite" in status
        assert status["postgres"]["status"] == "connected"
        assert status["sqlite"]["status"] == "connected"

    def test_engine_info(self):
        """Test engine configuration info retrieval."""
        info = get_engine_info()
        assert "postgres" in info
        assert "sqlite" in info
        assert info["postgres"]["pool_size"] > 0
        assert info["postgres"]["pool_pre_ping"] is True
        assert info["postgres"]["pool_recycle"] == 3600

    def test_engine_info_sqlite_config(self):
        """Test SQLite engine info is correct."""
        info = get_engine_info()
        sqlite_info = info["sqlite"]
        assert sqlite_info["pool_class"] == "NullPool"
        assert sqlite_info["timeout"] == 10


class TestEngineLifecycle:
    """Test engine lifecycle management."""

    @pytest.mark.asyncio
    async def test_dispose_engines(self):
        """Test engine disposal cleanup."""
        # This test ensures dispose_engines runs without error
        await dispose_engines()
        # Engines should still be usable after dispose (SQLAlchemy recreates pool)
        result = await test_postgres_connection()
        assert result is True


# Integration tests
class TestEngineIntegration:
    """Integration tests for the complete engine setup."""

    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """Test complete database access workflow."""
        # Test PostgreSQL access
        async with get_postgres_session() as pg_session:
            pg_result = await pg_session.execute(text("SELECT 1 as pg_test"))
            pg_value = pg_result.scalar()
            assert pg_value == 1

        # Test SQLite access
        async with get_sandbox_session() as sqlite_session:
            sqlite_result = await sqlite_session.execute(
                text("SELECT 1 as sqlite_test")
            )
            sqlite_value = sqlite_result.scalar()
            assert sqlite_value == 1

    @pytest.mark.asyncio
    async def test_engine_configuration_matches_settings(self):
        """Verify engine configuration matches application settings."""
        from app.config.settings import settings

        info = get_engine_info()
        assert info["postgres"]["pool_size"] == settings.DB_POOL_SIZE
        assert info["postgres"]["max_overflow"] == settings.DB_MAX_OVERFLOW

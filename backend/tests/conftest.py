"""Pytest fixtures and configuration."""

import pytest

from database.engine import dispose_engines


@pytest.fixture(autouse=True)
async def dispose_db_engines_after_test():
    """Dispose database engines after each async test.

    asyncpg connections are bound to the event loop that created them.
    Disposing the engine pool after each test prevents "event loop is closed"
    errors when pytest-asyncio creates a fresh event loop for the next test.
    """
    yield
    await dispose_engines()

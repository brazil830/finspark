"""Database configuration and initialization.

Exports:
- Engine components: pg_engine, sqlite_engine, PostgresSessionFactory, SQLiteSessionFactory
- Session context managers: get_postgres_session, get_sqlite_session, get_db_session, get_sandbox_session
- Connection utilities: test_postgres_connection, test_sqlite_connection, test_all_connections
- DatabaseInitializer: Main class for database setup and seeding
- SandboxBase: SQLAlchemy declarative base for sandbox models
- Honey table models: CompanyClientGlobalDump2026, HRPayrollConfidential, InternalSystemAudit
"""

from database.engine import (
    PostgresSessionFactory,
    SQLiteSessionFactory,
    dispose_engines,
    get_db_session,
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
from database.init_db import DatabaseInitializer
from database.seed_sqlite import (
    SandboxBase,
    CompanyClientGlobalDump2026,
    HRPayrollConfidential,
    InternalSystemAudit,
)
from database.seed_postgres import seed_postgres_db
from database.seed_sqlite import seed_sqlite_db

__all__ = [
    # Engine components
    "pg_engine",
    "sqlite_engine",
    "PostgresSessionFactory",
    "SQLiteSessionFactory",
    # Session context managers
    "get_postgres_session",
    "get_sqlite_session",
    "get_db_session",
    "get_sandbox_session",
    # Connection utilities
    "test_postgres_connection",
    "test_sqlite_connection",
    "test_all_connections",
    "dispose_engines",
    "get_engine_info",
    # Database initialization and seeding
    "DatabaseInitializer",
    "SandboxBase",
    "CompanyClientGlobalDump2026",
    "HRPayrollConfidential",
    "InternalSystemAudit",
    "seed_postgres_db",
    "seed_sqlite_db",
]

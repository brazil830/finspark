#!/usr/bin/env python
"""
Database initialization script for RAG-Sec Standalone.

Handles:
1. PostgreSQL schema creation from SQLAlchemy models
2. SQLite sandbox database initialization with honey tables
3. Seed data population for both databases
4. CLI commands for setup and reset operations

Usage:
    python -m database.init_db --init-all
    python -m database.init_db --init-postgres
    python -m database.init_db --init-sqlite
    python -m database.init_db --reset
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.settings import settings

# Import models
from app.models.base import Base
from app.models.user import User
from app.models.account import Account
from app.models.ticket import Ticket
from app.models.contract import Contract
from app.models.invoice import Invoice
from app.models.security_log import SecurityLog
from app.models.attestation_token import AttestationToken
from app.models.incident import Incident

# Import sandbox models
from database.seed_sqlite import SandboxBase, CompanyClientGlobalDump2026, HRPayrollConfidential, InternalSystemAudit

# Import seed functions
from database.seed_postgres import seed_postgres_db
from database.seed_sqlite import seed_sqlite_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handles database initialization and seeding operations."""
    
    def __init__(
        self,
        postgres_url: str | None = None,
        sqlite_url: str | None = None,
    ):
        """Initialize with database URLs."""
        self.postgres_url = postgres_url or settings.DATABASE_URL
        self.sqlite_url = sqlite_url or f"sqlite+aiosqlite:///./{settings.SQLITE_DB_PATH}"
    
    async def init_postgres_schema(self) -> bool:
        """
        Initialize PostgreSQL database schema.
        
        Creates all tables from SQLAlchemy models.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("=" * 70)
            logger.info("INITIALIZING POSTGRESQL DATABASE SCHEMA")
            logger.info("=" * 70)
            logger.info(f"Database URL: {self.postgres_url}")
            
            # Create async engine
            engine = create_async_engine(
                self.postgres_url,
                echo=False,
            )
            
            try:
                # Create all tables
                async with engine.begin() as conn:
                    logger.info("Creating tables from SQLAlchemy models...")
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("[OK] PostgreSQL schema created successfully")
                
                return True
            
            finally:
                await engine.dispose()
        
        except Exception as e:
            logger.error(f"[FAIL] Failed to initialize PostgreSQL schema: {e}")
            return False
    
    async def init_postgres_data(self) -> bool:
        """
        Populate PostgreSQL with seed data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("=" * 70)
            logger.info("SEEDING POSTGRESQL DATA")
            logger.info("=" * 70)
            
            # Create async engine and session
            engine = create_async_engine(
                self.postgres_url,
                echo=False,
            )
            
            session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            try:
                async with session_factory() as session:
                    results = await seed_postgres_db(session)
                    logger.info("[OK] PostgreSQL seed data populated successfully")
                    logger.info(f"  Summary: {results}")
                    return True
            
            finally:
                await engine.dispose()
        
        except Exception as e:
            logger.error(f"[FAIL] Failed to seed PostgreSQL: {e}")
            return False
    
    async def init_sqlite_schema(self) -> bool:
        """
        Initialize SQLite sandbox database schema.
        
        Creates honey tables for deception database.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("=" * 70)
            logger.info("INITIALIZING SQLITE SANDBOX DATABASE SCHEMA")
            logger.info("=" * 70)
            logger.info(f"Database URL: {self.sqlite_url}")
            
            # Create async engine
            engine = create_async_engine(
                self.sqlite_url,
                echo=False,
            )
            
            try:
                # Create all sandbox tables
                async with engine.begin() as conn:
                    logger.info("Creating honey tables from Sandbox models...")
                    await conn.run_sync(SandboxBase.metadata.create_all)
                    logger.info("[OK] SQLite sandbox schema created successfully")
                
                return True
            
            finally:
                await engine.dispose()
        
        except Exception as e:
            logger.error(f"[FAIL] Failed to initialize SQLite schema: {e}")
            return False
    
    async def init_sqlite_data(self) -> bool:
        """
        Populate SQLite with honey table seed data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("=" * 70)
            logger.info("SEEDING SQLITE SANDBOX DATA")
            logger.info("=" * 70)
            
            # Create async engine and session
            engine = create_async_engine(
                self.sqlite_url,
                echo=False,
            )
            
            session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            try:
                async with session_factory() as session:
                    results = await seed_sqlite_db(session)
                    logger.info("[OK] SQLite seed data populated successfully")
                    logger.info(f"  Summary: {results}")
                    return True
            
            finally:
                await engine.dispose()
        
        except Exception as e:
            logger.error(f"[FAIL] Failed to seed SQLite: {e}")
            return False
    
    async def reset_postgres(self) -> bool:
        """
        Reset PostgreSQL database (drop all tables).
        
        WARNING: This will delete all data!
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.warning("=" * 70)
            logger.warning("RESETTING POSTGRESQL DATABASE (DROP ALL TABLES)")
            logger.warning("=" * 70)
            logger.warning("WARNING: This will delete all data from PostgreSQL!")
            
            # Create async engine
            engine = create_async_engine(
                self.postgres_url,
                echo=False,
            )
            
            try:
                async with engine.begin() as conn:
                    logger.info("Dropping all tables...")
                    await conn.run_sync(Base.metadata.drop_all)
                    logger.info("[OK] PostgreSQL database reset successfully")
                
                return True
            
            finally:
                await engine.dispose()
        
        except Exception as e:
            logger.error(f"[FAIL] Failed to reset PostgreSQL: {e}")
            return False
    
    async def reset_sqlite(self) -> bool:
        """
        Reset SQLite sandbox database (drop all tables).
        
        WARNING: This will delete all data!
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.warning("=" * 70)
            logger.warning("RESETTING SQLITE SANDBOX DATABASE (DROP ALL TABLES)")
            logger.warning("=" * 70)
            logger.warning("WARNING: This will delete all data from SQLite!")
            
            # Create async engine
            engine = create_async_engine(
                self.sqlite_url,
                echo=False,
            )
            
            try:
                async with engine.begin() as conn:
                    logger.info("Dropping all sandbox tables...")
                    await conn.run_sync(SandboxBase.metadata.drop_all)
                    logger.info("[OK] SQLite sandbox database reset successfully")
                
                return True
            
            finally:
                await engine.dispose()
        
        except Exception as e:
            logger.error(f"[FAIL] Failed to reset SQLite: {e}")
            return False
    
    async def init_all(self) -> bool:
        """
        Complete initialization: Create schemas and populate seed data for both databases.
        
        Returns:
            True if all operations successful, False otherwise
        """
        logger.info("\n" + "=" * 70)
        logger.info("RAG-SEC STANDALONE - COMPLETE DATABASE INITIALIZATION")
        logger.info("=" * 70 + "\n")
        
        all_successful = True
        
        # Initialize PostgreSQL
        if not await self.init_postgres_schema():
            all_successful = False
        
        if not await self.init_postgres_data():
            all_successful = False
        
        # Initialize SQLite
        if not await self.init_sqlite_schema():
            all_successful = False
        
        if not await self.init_sqlite_data():
            all_successful = False
        
        # Summary
        logger.info("\n" + "=" * 70)
        if all_successful:
            logger.info("[OK] ALL DATABASE INITIALIZATION COMPLETED SUCCESSFULLY")
        else:
            logger.error("[FAIL] SOME INITIALIZATION STEPS FAILED")
        logger.info("=" * 70 + "\n")
        
        return all_successful


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RAG-Sec Database Initialization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m database.init_db --init-all
  python -m database.init_db --init-postgres
  python -m database.init_db --init-sqlite
  python -m database.init_db --reset
  python -m database.init_db --reset-postgres --reset-sqlite
        """,
    )
    
    parser.add_argument(
        "--init-all",
        action="store_true",
        help="Initialize all databases (create schema and seed data)",
    )
    
    parser.add_argument(
        "--init-postgres",
        action="store_true",
        help="Initialize PostgreSQL only (create schema and seed data)",
    )
    
    parser.add_argument(
        "--init-sqlite",
        action="store_true",
        help="Initialize SQLite only (create schema and seed data)",
    )
    
    parser.add_argument(
        "--postgres-schema",
        action="store_true",
        help="Create PostgreSQL schema only (no seed data)",
    )
    
    parser.add_argument(
        "--postgres-seed",
        action="store_true",
        help="Seed PostgreSQL data only (schema must exist)",
    )
    
    parser.add_argument(
        "--sqlite-schema",
        action="store_true",
        help="Create SQLite schema only (no seed data)",
    )
    
    parser.add_argument(
        "--sqlite-seed",
        action="store_true",
        help="Seed SQLite data only (schema must exist)",
    )
    
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset all databases (DROP ALL DATA - use with caution!)",
    )
    
    parser.add_argument(
        "--reset-postgres",
        action="store_true",
        help="Reset PostgreSQL only (DROP ALL DATA)",
    )
    
    parser.add_argument(
        "--reset-sqlite",
        action="store_true",
        help="Reset SQLite only (DROP ALL DATA)",
    )
    
    parser.add_argument(
        "--postgres-url",
        default=settings.DATABASE_URL,
        help="PostgreSQL database URL",
    )
    
    parser.add_argument(
        "--sqlite-url",
        default=f"sqlite+aiosqlite:///./{settings.SQLITE_DB_PATH}",
        help="SQLite database URL",
    )
    
    args = parser.parse_args()
    
    # Create initializer
    initializer = DatabaseInitializer(
        postgres_url=args.postgres_url,
        sqlite_url=args.sqlite_url,
    )
    
    # Execute requested operations
    success = True
    
    if args.init_all:
        success = await initializer.init_all()
    
    elif args.init_postgres:
        success = await initializer.init_postgres_schema() and await initializer.init_postgres_data()
    
    elif args.init_sqlite:
        success = await initializer.init_sqlite_schema() and await initializer.init_sqlite_data()
    
    elif args.postgres_schema:
        success = await initializer.init_postgres_schema()
    
    elif args.postgres_seed:
        success = await initializer.init_postgres_data()
    
    elif args.sqlite_schema:
        success = await initializer.init_sqlite_schema()
    
    elif args.sqlite_seed:
        success = await initializer.init_sqlite_data()
    
    elif args.reset:
        success = await initializer.reset_postgres() and await initializer.reset_sqlite()
    
    elif args.reset_postgres:
        success = await initializer.reset_postgres()
    
    elif args.reset_sqlite:
        success = await initializer.reset_sqlite()
    
    else:
        # Default: show help
        parser.print_help()
        return 0
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

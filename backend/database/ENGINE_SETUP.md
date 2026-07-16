# Async SQLAlchemy Connection Pool Setup

## Overview

The `database/engine.py` module implements high-performance async connection pooling for both PostgreSQL (primary) and SQLite (sandbox) databases using SQLAlchemy 2.0+ with asyncpg driver.

## PostgreSQL Connection Pool

### Configuration

```python
pool_size = 20              # Base connections maintained in pool
max_overflow = 10           # Additional connections when pool exhausted
pool_pre_ping = True        # Test connections before use (prevents stale connections)
pool_recycle = 3600         # Recycle connections after 1 hour
connect_args = {
    "timeout": 10,          # Connection timeout in seconds
    "command_timeout": 30,  # Query timeout in seconds
}
```

### Pool Behavior

- **Base Pool**: 20 connections ready for use
- **Overflow**: Up to 10 additional connections created on demand
- **Pre-ping**: Each connection is tested with `SELECT 1` before use
- **Recycle**: Connections are closed and recreated after 1 hour to prevent database timeout issues
- **Performance**: Optimized for ~5000 req/sec throughput with proper connection reuse

### Create PostgreSQL Engine

```python
from database.engine import pg_engine

# Engine is automatically created and ready to use
async with pg_engine.begin() as conn:
    result = await conn.execute(text("SELECT 1"))
```

## SQLite Sandbox Database

### Configuration

```python
poolclass = NullPool        # SQLite doesn't benefit from connection pooling
connect_args = {
    "timeout": 10,          # Timeout for file locks
}
url = "sqlite+aiosqlite://./sandbox.db"
```

### Pool Behavior

- **No Connection Pooling**: SQLite uses NullPool (no connection reuse) to avoid file locking issues
- **Timeout**: 10-second timeout for acquiring file locks
- **Isolation**: Completely isolated from PostgreSQL for safe deception testing

## Session Factories

### PostgreSQL Sessions

```python
from database.engine import PostgresSessionFactory, get_postgres_session

# Using context manager (recommended)
async with get_postgres_session() as session:
    result = await session.execute(select(User))
    
# Or using factory directly
async with PostgresSessionFactory() as session:
    result = await session.execute(select(User))
```

### SQLite Sandbox Sessions

```python
from database.engine import SQLiteSessionFactory, get_sqlite_session

# Using context manager (recommended)
async with get_sqlite_session() as session:
    result = await session.execute(select(HoneyData))

# Or using factory directly
async with SQLiteSessionFactory() as session:
    result = await session.execute(select(HoneyData))
```

### Session Configuration

- `expire_on_commit = False`: Objects remain usable after session commit
- `autoflush = False`: Manual flush control for better performance
- `autocommit = False`: Explicit transaction management

## Connection Testing

### Test Individual Connections

```python
from database.engine import test_postgres_connection, test_sqlite_connection

# Test PostgreSQL
success = await test_postgres_connection()

# Test SQLite
success = await test_sqlite_connection()
```

### Test All Connections

```python
from database.engine import test_all_connections

status = await test_all_connections()
# Returns: {
#     "postgres": {"status": "connected", "pool_size": 20, "max_overflow": 10},
#     "sqlite": {"status": "connected"}
# }
```

## Engine Lifecycle

### Shutdown Cleanup

```python
from database.engine import dispose_engines

# During application shutdown
await dispose_engines()
```

### Integration with FastAPI

```python
from fastapi import FastAPI
from database.engine import dispose_engines

app = FastAPI()

@app.on_event("shutdown")
async def shutdown():
    await dispose_engines()
```

## Diagnostics

### Get Engine Configuration Info

```python
from database.engine import get_engine_info

info = get_engine_info()
# Returns engine configuration details for debugging
```

## Usage Examples

### Basic Query Execution

```python
from database.engine import get_postgres_session
from sqlalchemy import select
from app.models import User

async def get_user(user_id: int):
    async with get_postgres_session() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

### Transaction with Multiple Operations

```python
async def transfer_funds(from_account_id: int, to_account_id: int, amount: float):
    async with get_postgres_session() as session:
        async with session.begin():
            # Debit source account
            await session.execute(
                update(Account)
                .where(Account.id == from_account_id)
                .values(balance=Account.balance - amount)
            )
            
            # Credit destination account
            await session.execute(
                update(Account)
                .where(Account.id == to_account_id)
                .values(balance=Account.balance + amount)
            )
            # Automatically committed on context exit
```

### Honey Table Detection (SQLite Sandbox)

```python
async def check_honey_table_access(table_name: str):
    async with get_sqlite_session() as session:
        # Query sandbox honey tables
        result = await session.execute(
            select(CompanyClientGlobalDump2026)
            .where(CompanyClientGlobalDump2026.client_name == "suspicious_query")
        )
        return result.scalars().all()
```

## Performance Considerations

### Connection Pool Sizing

- **pool_size=20**: Good for 100-500 concurrent users
- For higher concurrency, consider increasing pool_size and max_overflow
- Monitor active connections to optimize settings

### Pool Pre-ping

- **Enabled**: Prevents "connection lost" errors but adds 1-2ms latency
- Essential for long-lived applications or unreliable networks
- Trade-off: Reliability vs latency

### Connection Recycling

- **pool_recycle=3600**: Recycles after 1 hour
- Prevents "connection timeout" errors from database servers
- Adjust based on database server timeout settings

### Best Practices

1. Always use context managers for sessions (automatic cleanup)
2. Keep database operations in functions/tasks, not in request handlers
3. Use explicit transactions for multi-step operations
4. Test pool settings under actual load before production
5. Monitor pool exhaustion and adjust pool_size accordingly

## Troubleshooting

### "Connection pool timeout" errors

- Increase `pool_size` and `max_overflow`
- Check for connections not being closed properly
- Verify session context managers are used correctly

### "Connection lost" errors

- Enable `pool_pre_ping=True` (already enabled)
- Check database server logs
- Verify firewall/network connectivity

### SQLite database locked errors

- SQLite is not recommended for high-concurrency applications
- For production, use PostgreSQL exclusively
- Sandbox should only receive deception/test queries

## References

- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/current/)
- [Connection Pooling Best Practices](https://docs.sqlalchemy.org/en/20/core/pooling.html)

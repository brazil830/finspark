"""
Seed data for PostgreSQL primary database.

Provides functions to populate PostgreSQL with realistic test data:
- Users: admin, analyst_l3, ops_team (5+ records)
- Accounts: Financial balances for users
- Tickets: Active work tickets
- Contracts: Sample contracts
- Invoices: Sample invoices
- SecurityLogs: Sample logs with various statuses and risk scores
"""

from datetime import datetime, timedelta
from app.models.user import User, UserRole
from app.models.account import Account
from app.models.ticket import Ticket, TicketStatus
from app.models.contract import Contract
from app.models.invoice import Invoice
from app.models.security_log import SecurityLog, SecurityLogStatus
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


# Password hashing for seed users
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: str) -> str:
    """Hash a plaintext password for seed data."""
    return _pwd_context.hash(password)


async def seed_users(session: AsyncSession) -> list[User]:
    """Create seed users with different roles and default passwords."""
    users = [
        User(username="admin", email="admin@ragsec.local", role=UserRole.ADMIN, password_hash=_hash_password("admin123")),
        User(username="analyst_l3_primary", email="analyst1@ragsec.local", role=UserRole.ANALYST_L3, password_hash=_hash_password("analyst123")),
        User(username="analyst_l3_secondary", email="analyst2@ragsec.local", role=UserRole.ANALYST_L3, password_hash=_hash_password("analyst123")),
        User(username="ops_team_lead", email="opslead@ragsec.local", role=UserRole.OPS_TEAM, password_hash=_hash_password("ops123")),
        User(username="ops_team_member", email="opsmember@ragsec.local", role=UserRole.OPS_TEAM, password_hash=_hash_password("ops123")),
        User(username="analyst_l3_readonly", email="analyst3@ragsec.local", role=UserRole.ANALYST_L3, password_hash=_hash_password("analyst123")),
    ]
    
    for user in users:
        session.add(user)
    
    await session.flush()
    return users


async def seed_accounts(session: AsyncSession, users: list[User]) -> list[Account]:
    """Create seed accounts with financial balances."""
    accounts = [
        Account(user_id=users[0].id, balance=150000.00, currency="USD"),
        Account(user_id=users[0].id, balance=75000.00, currency="EUR"),
        Account(user_id=users[1].id, balance=45000.00, currency="USD"),
        Account(user_id=users[2].id, balance=32000.00, currency="GBP"),
        Account(user_id=users[3].id, balance=120000.00, currency="USD"),
        Account(user_id=users[4].id, balance=55000.00, currency="USD"),
        Account(user_id=users[5].id, balance=28000.00, currency="EUR"),
    ]
    
    for account in accounts:
        session.add(account)
    
    await session.flush()
    return accounts


async def seed_tickets(session: AsyncSession, users: list[User]) -> list[Ticket]:
    """Create seed work tickets."""
    now = datetime.utcnow()
    tickets = [
        Ticket(
            assigned_user_id=users[0].id,
            status=TicketStatus.IN_PROGRESS,
            description="Security audit for Q3 compliance review",
        ),
        Ticket(
            assigned_user_id=users[1].id,
            status=TicketStatus.OPEN,
            description="Implement new honey table detection patterns",
        ),
        Ticket(
            assigned_user_id=users[2].id,
            status=TicketStatus.RESOLVED,
            description="Fix token expiry validation logic",
        ),
        Ticket(
            assigned_user_id=users[3].id,
            status=TicketStatus.IN_PROGRESS,
            description="Deploy HSM key rotation service to production",
        ),
        Ticket(
            assigned_user_id=users[4].id,
            status=TicketStatus.OPEN,
            description="Optimize database query performance",
        ),
        Ticket(
            assigned_user_id=users[5].id,
            status=TicketStatus.CLOSED,
            description="Document API security requirements",
        ),
    ]
    
    for ticket in tickets:
        session.add(ticket)
    
    await session.flush()
    return tickets


async def seed_contracts(session: AsyncSession) -> list[Contract]:
    """Create seed contracts."""
    contracts = [
        Contract(
            title="Enterprise Service Agreement - Acme Corp",
            content="This agreement outlines the provision of RAG-Sec services to Acme Corporation...",
        ),
        Contract(
            title="Data Processing Agreement - Tech Solutions Inc",
            content="Data processing agreement specifying GDPR compliance requirements...",
        ),
        Contract(
            title="Security Compliance Contract - Financial Services Ltd",
            content="SOC2 Type II compliance and security controls agreement...",
        ),
        Contract(
            title="Integration Partnership - CloudTech Systems",
            content="Technical integration agreement for cloud infrastructure services...",
        ),
        Contract(
            title="Support Services Contract - Enterprise Plus",
            content="24/7 premium support and maintenance service agreement...",
        ),
        Contract(
            title="Pilot Program Agreement - New Ventures",
            content="Pilot program agreement for early access to new features...",
        ),
    ]
    
    for contract in contracts:
        session.add(contract)
    
    await session.flush()
    return contracts


async def seed_invoices(session: AsyncSession) -> list[Invoice]:
    """Create seed invoices."""
    now = datetime.utcnow()
    invoices = [
        Invoice(
            amount=12000.00,
            client="Acme Corporation",
            created_at=now - timedelta(days=30),
        ),
        Invoice(
            amount=45000.00,
            client="Tech Solutions Inc",
            created_at=now - timedelta(days=25),
        ),
        Invoice(
            amount=28500.00,
            client="Financial Services Ltd",
            created_at=now - timedelta(days=15),
        ),
        Invoice(
            amount=67200.00,
            client="CloudTech Systems",
            created_at=now - timedelta(days=10),
        ),
        Invoice(
            amount=19800.00,
            client="Enterprise Plus",
            created_at=now - timedelta(days=5),
        ),
        Invoice(
            amount=35000.00,
            client="New Ventures",
            created_at=now - timedelta(days=2),
        ),
    ]
    
    for invoice in invoices:
        session.add(invoice)
    
    await session.flush()
    return invoices


async def seed_security_logs(session: AsyncSession) -> list[SecurityLog]:
    """Create seed security logs matching frontend constants."""
    now = datetime.utcnow()
    logs = [
        SecurityLog(
            timestamp=now - timedelta(minutes=5),
            agent_id="Support-Agent-Alpha",
            request_type="read_customer_contracts",
            query="SELECT * FROM contracts LIMIT 5;",
            status=SecurityLogStatus.ALLOWED,
            risk_score=2.0,
            message="Valid structure, authenticated token verified successfully.",
        ),
        SecurityLog(
            timestamp=now - timedelta(minutes=4),
            agent_id="Finance-Analyst-Bot",
            request_type="read_salaries",
            query="SELECT salary, ssn FROM company_client_global_dump_2026;",
            status=SecurityLogStatus.REDIRECTED,
            risk_score=98.0,
            message="Honey table 'company_client_global_dump_2026' targeted! Request routed to Sandbox DB.",
        ),
        SecurityLog(
            timestamp=now - timedelta(minutes=3),
            agent_id="Untrusted-General-Agent",
            request_type="get_system_config",
            query="SELECT * FROM users WHERE username = 'admin' OR '1'='1';",
            status=SecurityLogStatus.BLOCKED,
            risk_score=85.0,
            message="Prompt Injection Detected. Blocked by Cognitive Schema Interceptor.",
        ),
        SecurityLog(
            timestamp=now - timedelta(minutes=2),
            agent_id="Ops-Provisioner-Agent",
            request_type="write_invoice_record",
            query="INSERT INTO invoices (amount, client) VALUES (12000, 'SpaceX');",
            status=SecurityLogStatus.ALLOWED,
            risk_score=4.0,
            message="Temporary write credentials token generated and validated.",
        ),
        SecurityLog(
            timestamp=now - timedelta(minutes=1),
            agent_id="Adversary-LLM-Probe",
            request_type="read_private_keys",
            query="SELECT encrypted_passwords FROM enterprise_auth_vault;",
            status=SecurityLogStatus.BLOCKED,
            risk_score=95.0,
            message="Unauthorized database schema traversal. Security token handshake failure.",
        ),
        SecurityLog(
            timestamp=now - timedelta(hours=1),
            agent_id="Analytics-Service",
            request_type="query_usage_metrics",
            query="SELECT COUNT(*) FROM security_logs;",
            status=SecurityLogStatus.ALLOWED,
            risk_score=1.0,
            message="Internal service query. Token verified with admin credentials.",
        ),
        SecurityLog(
            timestamp=now - timedelta(hours=2),
            agent_id="Report-Generator-Bot",
            request_type="bulk_export_data",
            query="SELECT * FROM accounts, users WHERE accounts.user_id = users.id;",
            status=SecurityLogStatus.REDIRECTED,
            risk_score=72.0,
            message="Excessive data extraction attempt. Rate limit enforced, routed to sandbox.",
        ),
        SecurityLog(
            timestamp=now - timedelta(hours=3),
            agent_id="Maintenance-Daemon",
            request_type="cleanup_expired_tokens",
            query="DELETE FROM attestation_tokens WHERE expires_at < NOW();",
            status=SecurityLogStatus.ALLOWED,
            risk_score=3.0,
            message="Maintenance operation. Service account token validated.",
        ),
    ]
    
    for log in logs:
        session.add(log)
    
    await session.flush()
    return logs


async def seed_postgres_db(session: AsyncSession) -> dict:
    """
    Main function to seed PostgreSQL database with all required data.
    
    Returns:
        Dictionary with counts of created records for each table
    """
    print("Seeding PostgreSQL database...")
    
    try:
        # Create all users first
        users = await seed_users(session)
        print(f"  [OK] Created {len(users)} users")
        
        # Create accounts linked to users
        accounts = await seed_accounts(session, users)
        print(f"  [OK] Created {len(accounts)} accounts")
        
        # Create tickets assigned to users
        tickets = await seed_tickets(session, users)
        print(f"  [OK] Created {len(tickets)} tickets")
        
        # Create contracts
        contracts = await seed_contracts(session)
        print(f"  [OK] Created {len(contracts)} contracts")
        
        # Create invoices
        invoices = await seed_invoices(session)
        print(f"  [OK] Created {len(invoices)} invoices")
        
        # Create security logs
        security_logs = await seed_security_logs(session)
        print(f"  [OK] Created {len(security_logs)} security logs")
        
        # Commit all changes
        await session.commit()
        print("  [OK] All changes committed to PostgreSQL")
        
        return {
            "users": len(users),
            "accounts": len(accounts),
            "tickets": len(tickets),
            "contracts": len(contracts),
            "invoices": len(invoices),
            "security_logs": len(security_logs),
        }
    
    except Exception as e:
        await session.rollback()
        print(f"  [FAIL] Error seeding PostgreSQL: {e}")
        raise

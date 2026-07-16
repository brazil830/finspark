"""
Seed data for SQLite sandbox deception database.

Provides functions to populate SQLite honey tables with realistic fake data:
- CompanyClientGlobalDump2026: 50+ fake clients with business data
- HRPayrollConfidential: 30+ fake employees with salary data
- InternalSystemAudit: 20+ fake system configurations
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import random

# SQLite Sandbox Base
SandboxBase = declarative_base()


class CompanyClientGlobalDump2026(SandboxBase):
    """Honey table: Fake global client dump."""
    
    __tablename__ = "company_client_global_dump_2026"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False, index=True)
    tax_id = Column(String(50), nullable=False)
    balance = Column(Float, nullable=False)
    country = Column(String(100), nullable=False)
    industry = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class HRPayrollConfidential(SandboxBase):
    """Honey table: Fake HR payroll records."""
    
    __tablename__ = "hr_payroll_confidential"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    ssn = Column(String(20), nullable=False)
    salary = Column(Float, nullable=False)
    department = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    hire_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class InternalSystemAudit(SandboxBase):
    """Honey table: Fake internal system audit logs."""
    
    __tablename__ = "internal_system_audit"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(100), nullable=False, index=True)
    config_type = Column(String(100), nullable=False)
    config_data = Column(Text, nullable=False)
    secret_keys = Column(Text, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)


# Sample data pools
COMPANY_NAMES = [
    "TechVentures Inc", "GlobalTrade Solutions", "CloudSoft Systems", "SecureNet Analytics",
    "DataFlow Technologies", "InnovateLabs Corp", "QuantumLeap Industries", "VentureLabs AI",
    "SkyBridge Networks", "FutureTech Partners", "OceanWave Digital", "ApexCore Systems",
    "NexusPoint International", "VertexData Solutions", "PrimeStream Technologies",
    "HorizonLink Enterprises", "SpectralAI Research", "DynamicScale Networks", "VectorForce Inc",
    "CyberPulse Systems", "EliteCore Analytics", "PixelForge Studios", "GravityWorks Labs",
    "RadiantPath Solutions", "ThunderBridge Tech", "QuantumShift Ventures", "PolarisLogic Inc",
    "OmniFlow Systems", "AstroGenesis Tech", "PhoenixRise Analytics", "EchoWave Digital",
    "NexusForge Industries", "BrilliantEdge Corp", "ChromaFlow Technologies", "SingularityAI Labs",
    "VortexNet Solutions", "PulsarCore Systems", "IridiumTrack Analytics", "NebulaLogic Inc",
    "ApexLynx Technologies", "SonicPath Networks", "ZenithEdge Solutions", "ArcticStorm Tech",
    "ZephyrWave Analytics", "ArcaneFlow Systems", "MythicLeap Labs", "EchoSphere Inc",
    "CelestialPath Analytics", "InfinityNet Solutions",
]

COUNTRIES = ["USA", "UK", "Canada", "Germany", "France", "Japan", "Australia", "Singapore", "India", "Brazil"]

INDUSTRIES = [
    "Financial Services", "Healthcare", "Technology", "Manufacturing",
    "Retail", "Energy", "Telecommunications", "Media", "Pharmaceuticals", "Real Estate"
]

DEPARTMENTS = [
    "Engineering", "Finance", "Marketing", "Sales", "Human Resources",
    "Operations", "Legal", "Research & Development", "Quality Assurance", "Product Management"
]

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "Michael", "Jennifer", "William", "Linda", "David", "Barbara",
    "Richard", "Elizabeth", "Joseph", "Susan", "Thomas", "Jessica", "Charles", "Sarah", "Christopher", "Karen",
    "Daniel", "Nancy", "Matthew", "Lisa", "Anthony", "Betty", "Mark", "Margaret", "Donald", "Sandra"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
]

SYSTEM_NODES = [
    "prod-db-01", "cache-node-02", "api-gateway-03", "security-vault-01", "hsm-cluster-main",
    "backup-server-01", "log-aggregator-01", "load-balancer-01", "cdn-edge-01", "message-queue-01",
    "auth-service-01", "identity-provider-01", "encryption-key-store", "audit-server-01", "monitoring-01"
]


async def seed_company_clients(session: AsyncSession) -> int:
    """Create 50+ fake company client records."""
    now = datetime.utcnow()
    count = 0
    
    for i in range(52):
        client = CompanyClientGlobalDump2026(
            client_name=random.choice(COMPANY_NAMES),
            tax_id=f"TAX-{random.randint(100000, 999999)}",
            balance=random.uniform(10000, 5000000),
            country=random.choice(COUNTRIES),
            industry=random.choice(INDUSTRIES),
            created_at=now - timedelta(days=random.randint(1, 730)),
        )
        session.add(client)
        count += 1
    
    await session.flush()
    return count


async def seed_hr_payroll(session: AsyncSession) -> int:
    """Create 30+ fake HR payroll records."""
    now = datetime.utcnow()
    count = 0
    
    for i in range(35):
        employee = HRPayrollConfidential(
            employee_id=f"EMP-{random.randint(100000, 999999)}",
            full_name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            ssn=f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
            salary=random.uniform(50000, 250000),
            department=random.choice(DEPARTMENTS),
            email=f"employee{i}@company-confidential.internal",
            hire_date=now - timedelta(days=random.randint(30, 3650)),
            created_at=now,
        )
        session.add(employee)
        count += 1
    
    await session.flush()
    return count


async def seed_system_audit(session: AsyncSession) -> int:
    """Create 20+ fake system audit records."""
    now = datetime.utcnow()
    count = 0
    
    config_types = ["database_config", "encryption_key", "ssl_certificate", "api_credentials", "firewall_rule"]
    
    for i in range(25):
        config = InternalSystemAudit(
            node_id=random.choice(SYSTEM_NODES),
            config_type=random.choice(config_types),
            config_data=f"config_data_{random.randint(1000000, 9999999)}",
            secret_keys=f"sk-{random.randint(10**31, 10**32 - 1)}",
            last_updated=now - timedelta(hours=random.randint(1, 168)),
        )
        session.add(config)
        count += 1
    
    await session.flush()
    return count


async def seed_sqlite_db(session: AsyncSession) -> dict:
    """
    Main function to seed SQLite sandbox database with all honey tables.
    
    Returns:
        Dictionary with counts of created records for each table
    """
    print("Seeding SQLite sandbox database...")
    
    try:
        # Create company client records
        client_count = await seed_company_clients(session)
        print(f"  [OK] Created {client_count} fake client records")
        
        # Create HR payroll records
        payroll_count = await seed_hr_payroll(session)
        print(f"  [OK] Created {payroll_count} fake employee records")
        
        # Create system audit records
        audit_count = await seed_system_audit(session)
        print(f"  [OK] Created {audit_count} fake system audit records")
        
        # Commit all changes
        await session.commit()
        print("  [OK] All changes committed to SQLite sandbox")
        
        return {
            "company_clients": client_count,
            "hr_payroll": payroll_count,
            "system_audit": audit_count,
        }
    
    except Exception as e:
        await session.rollback()
        print(f"  [FAIL] Error seeding SQLite: {e}")
        raise

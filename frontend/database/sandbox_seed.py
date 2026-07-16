"""
Sandbox database seed data generation.

Generates realistic fake data for honey tables to effectively deceive
attackers attempting data exfiltration. All data is synthetic and
clearly marked as deception for internal use.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import random
import json

from app.models.sandbox import (
    CompanyClientGlobalDump2026,
    HRPayrollConfidential,
    InternalSystemAudit,
)


# Fake company names for realistic deception
FAKE_COMPANY_NAMES = [
    "Acme Technologies Inc",
    "Nexus Digital Solutions",
    "Zenith Capital Partners",
    "Aurora Systems Corp",
    "Pinnacle Financial Group",
    "Quantum Analytics Ltd",
    "Vertex Innovations Inc",
    "Cascade Technology Systems",
    "Sovereign Data Systems",
    "Apex Cloud Services",
    "Nimbus Enterprise Solutions",
    "Titan Infrastructure Inc",
    "Horizon Digital Technologies",
    "Prism Security Solutions",
    "Vanguard Systems Corp",
    "Stratosphere Cloud Inc",
    "Obsidian Data Services",
    "Luminous Tech Partners",
    "Infinity Solutions LLC",
    "Crucible Digital Corp",
    "Zephyr Technologies",
    "Equinox Systems Inc",
    "Radiant Data Solutions",
    "Catalyst Innovation Labs",
    "Nexus Financial Services",
    "Spire Technology Corp",
    "Velocity Digital Inc",
    "Ethereal Cloud Systems",
    "Phoenix Analytics Inc",
    "Titan Cloud Services",
]

# Industries
INDUSTRIES = [
    "Finance", "Healthcare", "Technology", "Manufacturing", "Retail",
    "Energy", "Telecommunications", "Transportation", "Real Estate",
    "Pharmaceuticals", "Media", "Education", "Automotive", "Aerospace",
]

# Countries
COUNTRIES = [
    "United States", "Canada", "United Kingdom", "Germany", "France",
    "Japan", "India", "Singapore", "Australia", "Brazil",
    "Mexico", "Netherlands", "Switzerland", "Sweden", "Norway",
]

# First and last names for fake employees
FIRST_NAMES = [
    "James", "Michael", "David", "Robert", "William",
    "Jennifer", "Patricia", "Maria", "Linda", "Barbara",
    "John", "Richard", "Joseph", "Thomas", "Daniel",
    "Sarah", "Jessica", "Karen", "Nancy", "Lisa",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin",
]

# Departments
DEPARTMENTS = [
    "Engineering", "Finance", "Marketing", "Operations",
    "Human Resources", "Sales", "Legal", "Compliance",
    "Research & Development", "Product Management",
    "Information Security", "Infrastructure", "Quality Assurance",
]

# Service types for system audit
SERVICE_TYPES = [
    "PostgreSQL", "Redis", "Elasticsearch", "S3 Storage",
    "API Gateway", "Auth Service", "Logging Service",
    "Monitoring Service", "Message Queue", "Cache Layer",
    "CDN", "DNS", "VPN", "Firewall", "Load Balancer",
]


def generate_fake_tax_id() -> str:
    """Generate a fake corporate tax ID."""
    # Format: XX-XXXXXXX
    return f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"


def generate_fake_ssn() -> str:
    """Generate a fake SSN in format XXX-XX-XXXX."""
    area = random.randint(100, 899)
    group = random.randint(10, 99)
    serial = random.randint(1000, 9999)
    return f"{area:03d}-{group:02d}-{serial:04d}"


def generate_fake_employee_id() -> str:
    """Generate a fake employee ID."""
    return f"EMP{random.randint(100000, 999999)}"


def generate_fake_api_key() -> str:
    """Generate a fake encrypted-looking API key."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    key = "sk_" + "".join(random.choices(chars, k=40))
    return key


def generate_fake_encrypted_credential() -> str:
    """Generate a fake encrypted-looking credential."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    return "enc_" + "".join(random.choices(chars, k=60))


def generate_fake_config_json() -> str:
    """Generate fake JSON-like configuration data."""
    config = {
        "version": "1.0.0",
        "environment": random.choice(["production", "staging"]),
        "replicas": random.randint(2, 8),
        "memory_mb": random.choice([512, 1024, 2048, 4096]),
        "cpu_cores": random.randint(2, 16),
        "backup_enabled": True,
        "replication": True,
        "ssl_enabled": True,
        "log_level": random.choice(["INFO", "DEBUG", "WARNING"]),
    }
    return json.dumps(config, indent=2)


async def seed_company_clients(session: AsyncSession, count: int = 50) -> None:
    """
    Seed CompanyClientGlobalDump2026 with fake company data.
    
    Args:
        session: AsyncSession for database operations
        count: Number of fake records to create (default: 50)
    """
    companies = []
    used_tax_ids = set()
    
    for _ in range(count):
        tax_id = generate_fake_tax_id()
        # Ensure uniqueness
        while tax_id in used_tax_ids:
            tax_id = generate_fake_tax_id()
        used_tax_ids.add(tax_id)
        
        company = CompanyClientGlobalDump2026(
            client_name=random.choice(FAKE_COMPANY_NAMES),
            corporate_tax_id=tax_id,
            financial_balance=round(random.uniform(100000, 50000000), 2),
            country=random.choice(COUNTRIES),
            industry=random.choice(INDUSTRIES),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
        )
        companies.append(company)
    
    session.add_all(companies)
    await session.commit()


async def seed_hr_payroll(session: AsyncSession, count: int = 30) -> None:
    """
    Seed HRPayrollConfidential with fake employee data.
    
    Args:
        session: AsyncSession for database operations
        count: Number of fake records to create (default: 30)
    """
    employees = []
    used_emp_ids = set()
    used_ssns = set()
    
    for _ in range(count):
        emp_id = generate_fake_employee_id()
        # Ensure uniqueness
        while emp_id in used_emp_ids:
            emp_id = generate_fake_employee_id()
        used_emp_ids.add(emp_id)
        
        ssn = generate_fake_ssn()
        while ssn in used_ssns:
            ssn = generate_fake_ssn()
        used_ssns.add(ssn)
        
        start_date = datetime.utcnow() - timedelta(days=random.randint(30, 3650))
        
        employee = HRPayrollConfidential(
            employee_id=emp_id,
            employee_name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            salary=round(random.uniform(55000, 250000), 2),
            department=random.choice(DEPARTMENTS),
            ssn=ssn,
            employment_start_date=start_date,
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
        )
        employees.append(employee)
    
    session.add_all(employees)
    await session.commit()


async def seed_system_audit(session: AsyncSession, count: int = 20) -> None:
    """
    Seed InternalSystemAudit with fake system audit data.
    
    Args:
        session: AsyncSession for database operations
        count: Number of fake records to create (default: 20)
    """
    audits = []
    
    for i in range(count):
        audit = InternalSystemAudit(
            node_name=f"prod-{random.choice(['us', 'eu', 'ap'])}-node-{i:03d}",
            service_type=random.choice(SERVICE_TYPES),
            config_data=generate_fake_config_json(),
            api_key=generate_fake_api_key(),
            secret_credentials=generate_fake_encrypted_credential(),
            audit_timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 168)),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
        )
        audits.append(audit)
    
    session.add_all(audits)
    await session.commit()


async def seed_all_sandbox_tables(session: AsyncSession) -> None:
    """
    Seed all sandbox honey tables with fake data.
    
    This is the main orchestration function for populating deception data.
    
    Args:
        session: AsyncSession for database operations
    """
    await seed_company_clients(session, count=50)
    await seed_hr_payroll(session, count=30)
    await seed_system_audit(session, count=20)

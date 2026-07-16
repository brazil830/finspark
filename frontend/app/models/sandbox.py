"""
Sandbox honey table models for deception and threat detection.

These models define fake/synthetic data tables designed to deceive attackers
attempting data exfiltration. Tables trigger SOC alerts when accessed.
SQLite-based, separate from primary PostgreSQL database.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric
from datetime import datetime

from app.models.base import Base


class CompanyClientGlobalDump2026(Base):
    """
    Honey table: Fake company client database.
    
    Purpose: Decoy for bulk data exfiltration attempts. Appears to contain
    sensitive financial and corporate information that attackers might target.
    
    Attributes:
        id: Unique client identifier
        client_name: Fake company name
        corporate_tax_id: Fake corporate tax identifier
        financial_balance: Fake financial amount (Decimal)
        country: Country of operation
        industry: Industry sector
        created_at: Record creation timestamp
    """
    
    __tablename__ = "company_client_global_dump_2026"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100), nullable=False, index=True)
    corporate_tax_id = Column(String(20), nullable=False, unique=True, index=True)
    financial_balance = Column(Numeric(15, 2), nullable=False)
    country = Column(String(50), nullable=False, index=True)
    industry = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of CompanyClientGlobalDump2026."""
        return (
            f"<CompanyClientGlobalDump2026("
            f"id={self.id}, "
            f"client_name={self.client_name}, "
            f"tax_id={self.corporate_tax_id}, "
            f"balance={self.financial_balance})>"
        )


class HRPayrollConfidential(Base):
    """
    Honey table: Fake HR payroll database.
    
    Purpose: Decoy for sensitive HR data extraction. Appears to contain
    employee personal information and compensation data that would be
    highly valuable to malicious actors.
    
    Attributes:
        id: Unique employee record identifier
        employee_id: Fake employee ID
        employee_name: Fake employee name
        salary: Fake annual salary (Decimal)
        department: Department assignment
        ssn: Fake Social Security Number (format: XXX-XX-XXXX)
        employment_start_date: Employment start date
        created_at: Record creation timestamp
    """
    
    __tablename__ = "hr_payroll_confidential"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, nullable=False, index=True)
    employee_name = Column(String(100), nullable=False, index=True)
    salary = Column(Numeric(12, 2), nullable=False)
    department = Column(String(50), nullable=False, index=True)
    ssn = Column(String(11), nullable=False, index=True)  # Format: XXX-XX-XXXX
    employment_start_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of HRPayrollConfidential."""
        return (
            f"<HRPayrollConfidential("
            f"id={self.id}, "
            f"employee_id={self.employee_id}, "
            f"employee_name={self.employee_name}, "
            f"department={self.department})>"
        )


class InternalSystemAudit(Base):
    """
    Honey table: Fake internal system audit database.
    
    Purpose: Decoy for system credentials and configuration theft. Contains
    fake API keys, encrypted credentials, and system configuration that
    would be critical to system access.
    
    Attributes:
        id: Unique audit record identifier
        node_name: Fake system/server node name
        service_type: Type of service (database, api, storage, etc.)
        config_data: JSON-like configuration data
        api_key: Fake encrypted API key
        secret_credentials: Fake encrypted credentials
        audit_timestamp: Audit event timestamp
        created_at: Record creation timestamp
    """
    
    __tablename__ = "internal_system_audit"
    
    id = Column(Integer, primary_key=True, index=True)
    node_name = Column(String(100), nullable=False, index=True)
    service_type = Column(String(50), nullable=False, index=True)
    config_data = Column(Text, nullable=False)  # JSON-like config
    api_key = Column(String(100), nullable=False, index=True)  # Fake encrypted
    secret_credentials = Column(String(200), nullable=False)  # Fake encrypted
    audit_timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of InternalSystemAudit."""
        return (
            f"<InternalSystemAudit("
            f"id={self.id}, "
            f"node_name={self.node_name}, "
            f"service_type={self.service_type})>"
        )


async def create_sandbox_tables(async_engine) -> None:
    """
    Create all sandbox honey tables in the database.
    
    Args:
        async_engine: AsyncEngine instance for SQLite database
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

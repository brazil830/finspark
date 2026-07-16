"""Database models.

SQLAlchemy ORM models for RAG-Sec backend with async support.
All models inherit from BaseModel providing id, created_at, updated_at.
"""

from app.models.base import Base, BaseModel
from app.models.user import User, UserRole
from app.models.account import Account
from app.models.ticket import Ticket, TicketStatus
from app.models.contract import Contract
from app.models.invoice import Invoice, InvoiceStatus
from app.models.attestation_token import AttestationToken
from app.models.security_log import SecurityLog, SecurityLogStatus
from app.models.incident import Incident, IncidentStatus

__all__ = [
    # Base
    "Base",
    "BaseModel",
    # User & Auth
    "User",
    "UserRole",
    # Accounts & Financial
    "Account",
    "Invoice",
    "InvoiceStatus",
    # Tickets & Operations
    "Ticket",
    "TicketStatus",
    # Contracts
    "Contract",
    # Security & Attestation
    "AttestationToken",
    "SecurityLog",
    "SecurityLogStatus",
    # Incidents
    "Incident",
    "IncidentStatus",
]

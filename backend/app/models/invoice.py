"""Invoice model for managing invoices and billing."""

from decimal import Decimal
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import DECIMAL, Enum, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class InvoiceStatus(str, PyEnum):
    """Enumeration of invoice statuses."""

    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(BaseModel):
    """Invoice model for billing and financial tracking.
    
    Represents an invoice issued to a client with amount and status tracking.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        amount: Invoice amount (Decimal for financial precision)
        client: Client name or identifier
        status: Invoice status (draft, sent, paid, overdue, cancelled)
        created_at: Record creation timestamp (inherited from BaseModel)
        updated_at: Record update timestamp (inherited from BaseModel)
    """

    __tablename__ = "invoices"

    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=18, scale=2),
        nullable=False,
    )
    client: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus),
        default=InvoiceStatus.DRAFT,
        nullable=False,
        index=True,
    )

    # Indexes
    __table_args__ = (
        Index("idx_invoices_client", "client"),
        Index("idx_invoices_status", "status"),
        Index("idx_invoices_created_at", "created_at"),
        Index("idx_invoices_client_status", "client", "status"),
    )

    def __repr__(self) -> str:
        """Return string representation of invoice."""
        return (
            f"<Invoice(id={self.id}, amount={self.amount}, "
            f"client={self.client}, status={self.status})>"
        )

"""
Invoice model for financial transaction tracking.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from app.models.base import Base


class Invoice(Base):
    """
    Invoice model representing financial invoices.
    
    Attributes:
        id: Unique invoice identifier
        amount: Invoice amount
        client: Client name
        created_at: Timestamp of invoice creation
    """
    
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    client = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of Invoice."""
        return f"<Invoice(id={self.id}, amount={self.amount}, client={self.client})>"

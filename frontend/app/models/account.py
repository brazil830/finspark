"""
Account model for financial tracking.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Account(Base):
    """
    Account model representing user financial accounts.
    
    Attributes:
        id: Unique account identifier
        user_id: Foreign key to User
        balance: Current account balance
        currency: Currency code (e.g., USD, EUR)
        created_at: Timestamp of account creation
    """
    
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    
    def __repr__(self) -> str:
        """String representation of Account."""
        return f"<Account(id={self.id}, user_id={self.user_id}, balance={self.balance}, currency={self.currency})>"

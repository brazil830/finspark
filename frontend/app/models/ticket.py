"""
Ticket model for work request tracking.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


class TicketStatus(str, enum.Enum):
    """Ticket status enumeration."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Ticket(Base):
    """
    Ticket model representing work requests and tasks.
    
    Attributes:
        id: Unique ticket identifier
        assigned_user_id: Foreign key to User
        status: Current ticket status
        description: Ticket description
        created_at: Timestamp of ticket creation
    """
    
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assigned_user = relationship("User", back_populates="tickets")
    
    def __repr__(self) -> str:
        """String representation of Ticket."""
        return f"<Ticket(id={self.id}, assigned_user_id={self.assigned_user_id}, status={self.status})>"

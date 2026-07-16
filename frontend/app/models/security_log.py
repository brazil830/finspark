"""
Security log model for audit trail and incident tracking.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Enum
from datetime import datetime
import enum

from app.models.base import Base


class RequestStatus(str, enum.Enum):
    """Request status enumeration."""
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    REDIRECTED = "REDIRECTED"


class SecurityLog(Base):
    """
    Security log model for tracking and auditing all security-relevant events.
    
    Attributes:
        id: Unique log identifier
        timestamp: When the event occurred
        agent_id: ID of the agent that made the request
        request_type: Type of request (e.g., read_customer_contracts)
        query: The actual query/request that was made
        status: Whether the request was ALLOWED, BLOCKED, or REDIRECTED
        risk_score: Risk score (0-100) assigned to the request
        message: Detailed message about the event
    """
    
    __tablename__ = "security_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    agent_id = Column(String(255), index=True, nullable=False)
    request_type = Column(String(255), nullable=False)
    query = Column(Text, nullable=True)
    status = Column(Enum(RequestStatus), nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    message = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        """String representation of SecurityLog."""
        return f"<SecurityLog(id={self.id}, agent_id={self.agent_id}, status={self.status}, risk_score={self.risk_score})>"

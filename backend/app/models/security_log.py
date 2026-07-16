"""SecurityLog model for audit logging security events."""

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class SecurityLogStatus(str, PyEnum):
    """Enumeration of security log statuses."""

    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    REDIRECTED = "REDIRECTED"


class SecurityLog(BaseModel):
    """SecurityLog model for comprehensive security audit logging.
    
    Tracks all security-relevant events including agent queries, validation results,
    and threat detections. Critical for audit trail and SOC monitoring.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        timestamp: When the security event occurred
        agent_id: Identifier for the AI agent making the request
        request_type: Type of request (e.g., QUERY, EXECUTE, VALIDATE)
        query: The query or command that triggered the log entry
        status: Security decision (ALLOWED, BLOCKED, REDIRECTED)
        risk_score: Risk assessment score (0.0-1.0)
        message: Human-readable security decision message
        user_id: Optional foreign key to User table (operator performing action)
        created_at: Record creation timestamp (inherited from BaseModel)
    
    Relationships:
        user: Optional many-to-one relationship with User model
    
    Purpose:
        - Complete audit trail of all security decisions
        - SOC alerts and threat detection
        - Performance metrics and analytics
        - Compliance and regulatory reporting
    """

    __tablename__ = "security_logs"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    agent_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    request_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    query: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[SecurityLogStatus] = mapped_column(
        Enum(SecurityLogStatus),
        nullable=False,
        index=True,
    )
    risk_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="security_logs",
    )

    # Indexes
    __table_args__ = (
        Index("idx_security_logs_timestamp", "timestamp"),
        Index("idx_security_logs_agent_id", "agent_id"),
        Index("idx_security_logs_status", "status"),
        Index("idx_security_logs_user_id", "user_id"),
        Index("idx_security_logs_timestamp_status", "timestamp", "status"),
        Index("idx_security_logs_agent_status", "agent_id", "status"),
    )

    def __repr__(self) -> str:
        """Return string representation of security log."""
        return (
            f"<SecurityLog(id={self.id}, agent_id={self.agent_id}, "
            f"status={self.status}, risk_score={self.risk_score})>"
        )

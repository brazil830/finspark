"""Incident model for tracking honey table detection events."""

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, Float, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class IncidentStatus(str, PyEnum):
    """Enumeration of incident statuses."""

    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class Incident(BaseModel):
    """Incident model for tracking security incidents.
    
    Records all detected honey table access attempts and security threats
    for audit trail and SOC monitoring.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        timestamp: When the incident was detected
        agent_id: Identifier for the AI agent that triggered the incident
        query: The query that triggered the incident
        honey_table: Name of honey table accessed (if applicable)
        status: Incident status (DETECTED, INVESTIGATING, RESOLVED, FALSE_POSITIVE)
        risk_score: Risk assessment score (0.0-1.0)
        sandbox_routed: Whether request was routed to sandbox
        fake_data_served: Whether fake data was served
        user_id: Optional user who owns the session
        created_at: Record creation timestamp (inherited from BaseModel)
        updated_at: Record update timestamp (inherited from BaseModel)
    
    Relationships:
        user: Optional many-to-one relationship with User model
    """

    __tablename__ = "incidents"

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
    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    honey_table: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus),
        default=IncidentStatus.DETECTED,
        nullable=False,
        index=True,
    )
    risk_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    sandbox_routed: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    fake_data_served: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Indexes for common queries
    __table_args__ = (
        Index("idx_incidents_timestamp_status", "timestamp", "status"),
        Index("idx_incidents_agent_id", "agent_id"),
        Index("idx_incidents_risk_score", "risk_score"),
    )

    def __repr__(self) -> str:
        """Return string representation of incident."""
        return (
            f"<Incident(id={self.id}, agent_id={self.agent_id}, "
            f"status={self.status}, risk_score={self.risk_score})>"
        )
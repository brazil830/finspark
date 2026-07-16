"""Ticket model for tracking operational tickets and tasks."""

from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class TicketStatus(str, PyEnum):
    """Enumeration of ticket statuses."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    RESOLVED = "resolved"


class Ticket(BaseModel):
    """Ticket model for operational task tracking.
    
    Represents a support or operational ticket assigned to a user.
    Tracks ticket status and description.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        assigned_user_id: Foreign key to User table (assigned operator)
        status: Ticket status (open, in_progress, closed, resolved)
        description: Detailed description of the ticket
        created_at: Record creation timestamp (inherited from BaseModel)
        updated_at: Record update timestamp (inherited from BaseModel)
    
    Relationships:
        assigned_user: Many-to-one relationship with User model
    """

    __tablename__ = "tickets"

    assigned_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus),
        default=TicketStatus.OPEN,
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    assigned_user: Mapped["User"] = relationship(
        "User",
        back_populates="tickets",
    )

    # Indexes
    __table_args__ = (
        Index("idx_tickets_assigned_user_id", "assigned_user_id"),
        Index("idx_tickets_status", "status"),
        Index("idx_tickets_status_user", "status", "assigned_user_id"),
    )

    def __repr__(self) -> str:
        """Return string representation of ticket."""
        return (
            f"<Ticket(id={self.id}, assigned_user_id={self.assigned_user_id}, "
            f"status={self.status})>"
        )

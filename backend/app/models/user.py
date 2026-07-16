"""User model for authentication and role management."""

from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone

from sqlalchemy import Enum, String, UniqueConstraint, Index, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.ticket import Ticket
    from app.models.security_log import SecurityLog


class UserRole(str, PyEnum):
    """Enumeration of user roles in the system."""

    ADMIN = "admin"
    ANALYST_L3 = "analyst_l3"
    OPS_TEAM = "ops_team"


class User(BaseModel):
    """User model for authentication and authorization.
    
    Represents a user in the system with role-based access control.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        username: Unique username identifier
        email: Email address
        password_hash: Bcrypt hashed password (nullable for backward compatibility)
        full_name: Optional full name of the user
        role: User role (admin, analyst_l3, ops_team)
        is_active: Whether user account is active
        last_login: Timestamp of last login
        created_at: Record creation timestamp (inherited from BaseModel)
        updated_at: Record update timestamp (inherited from BaseModel)
    
    Relationships:
        accounts: One-to-many relationship with Account model
        tickets: One-to-many relationship with Ticket model (assigned tickets)
        security_logs: One-to-many relationship with SecurityLog model
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    password_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.OPS_TEAM,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    accounts: Mapped[List["Account"]] = relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        back_populates="assigned_user",
        cascade="all, delete-orphan",
    )
    security_logs: Mapped[List["SecurityLog"]] = relationship(
        "SecurityLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Indexes
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
        Index("idx_users_role", "role"),
        Index("idx_users_is_active", "is_active"),
    )

    def __repr__(self) -> str:
        """Return string representation of user."""
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

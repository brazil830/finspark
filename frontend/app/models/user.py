"""
User model for authentication and role-based access control.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    ANALYST_L3 = "analyst_l3"
    ANALYST_L2 = "analyst_l2"
    OPS = "ops"
    GUEST = "guest"


class User(Base):
    """
    User model representing authenticated users in the system.
    
    Attributes:
        id: Unique user identifier
        username: Unique username for login
        role: User role (admin, analyst_l3, analyst_l2, ops, guest)
        created_at: Timestamp of user creation
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.GUEST, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    accounts = relationship("Account", back_populates="user")
    tickets = relationship("Ticket", back_populates="assigned_user")
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

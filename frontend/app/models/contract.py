"""
Contract model for storing business contracts.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.models.base import Base


class Contract(Base):
    """
    Contract model representing business contracts.
    
    Attributes:
        id: Unique contract identifier
        title: Contract title
        content: Full contract content
        created_at: Timestamp of contract creation
    """
    
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of Contract."""
        return f"<Contract(id={self.id}, title={self.title})>"

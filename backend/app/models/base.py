"""Base model class with common fields."""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class BaseModel(Base):
    """Base class for all SQLAlchemy models with common fields.
    
    Provides:
    - id: Primary key (Integer)
    - created_at: Timestamp when record was created (DateTime)
    - updated_at: Timestamp when record was last updated (DateTime)
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Return string representation of model instance."""
        return f"<{self.__class__.__name__}(id={self.id})>"

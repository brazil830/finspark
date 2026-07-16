"""Contract model for managing contracts and agreements."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.account import Account


class Contract(BaseModel):
    """Contract model for managing contracts and agreements.
    
    Represents a contract or agreement in the system,
    optionally linked to a client account.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        title: Contract title
        content: Full contract content
        client_id: Optional foreign key to Account table (client reference)
        created_at: Record creation timestamp (inherited from BaseModel)
        updated_at: Record update timestamp (inherited from BaseModel)
    
    Relationships:
        client_account: Optional one-to-one relationship with Account model
    """

    __tablename__ = "contracts"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    client_account: Mapped[Optional["Account"]] = relationship(
        "Account",
    )

    # Indexes
    __table_args__ = (
        Index("idx_contracts_client_id", "client_id"),
        Index("idx_contracts_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        """Return string representation of contract."""
        return (
            f"<Contract(id={self.id}, title={self.title}, "
            f"client_id={self.client_id})>"
        )

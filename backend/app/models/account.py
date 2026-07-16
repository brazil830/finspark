"""Account model for managing user accounts and balance tracking."""

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DECIMAL, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Account(BaseModel):
    """Account model for user account and balance management.
    
    Represents a financial account associated with a user,
    tracking balance and currency.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        user_id: Foreign key to User table
        balance: Account balance (Decimal for financial precision)
        currency: Currency code (e.g., USD, EUR, GBP)
        created_at: Record creation timestamp (inherited from BaseModel)
        updated_at: Record update timestamp (inherited from BaseModel)
    
    Relationships:
        user: Many-to-one relationship with User model
    """

    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=18, scale=2),
        default=Decimal("0.00"),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="USD",
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts",
    )

    # Indexes
    __table_args__ = (
        Index("idx_accounts_user_id", "user_id"),
        Index("idx_accounts_currency", "currency"),
    )

    def __repr__(self) -> str:
        """Return string representation of account."""
        return (
            f"<Account(id={self.id}, user_id={self.user_id}, "
            f"balance={self.balance} {self.currency})>"
        )

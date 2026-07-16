"""AttestationToken model for tracking issued security tokens."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AttestationToken(BaseModel):
    """AttestationToken model for audit logging and token tracking.
    
    Tracks issued HMAC-SHA256 tokens for attestation and audit purposes.
    Tokens have an expiration window and are used to validate AI agent requests.
    
    Fields:
        id: Primary key (inherited from BaseModel)
        token_hash: Hashed token value (unique, indexed for fast lookup)
        session_id: Session identifier this token was issued for
        payload_hash: Hash of the token payload for validation
        expires_at: Timestamp when this token expires
        created_at: Record creation timestamp (inherited from BaseModel)
    
    Purpose:
        - Audit trail for all issued tokens
        - Fast token lookup by token_hash
        - Session tracking and validation
        - Expiration management and cleanup
    """

    __tablename__ = "attestation_tokens"

    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    session_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    payload_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # Indexes
    __table_args__ = (
        Index("idx_attestation_tokens_token_hash", "token_hash"),
        Index("idx_attestation_tokens_session_id", "session_id"),
        Index("idx_attestation_tokens_expires_at", "expires_at"),
        Index("idx_attestation_tokens_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        """Return string representation of attestation token."""
        return (
            f"<AttestationToken(id={self.id}, session_id={self.session_id}, "
            f"expires_at={self.expires_at})>"
        )

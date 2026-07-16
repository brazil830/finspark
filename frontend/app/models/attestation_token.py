"""
Attestation token model for tracking cryptographic tokens.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.models.base import Base


class AttestationToken(Base):
    """
    Attestation token model for tracking issued HMAC-SHA256 tokens.
    
    Attributes:
        id: Unique token identifier
        token_hash: HMAC-SHA256 hash of the token
        session_id: Session ID associated with the token
        payload_hash: Hash of the token payload
        expires_at: Expiration timestamp
        created_at: Timestamp of token creation
    """
    
    __tablename__ = "attestation_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(255), unique=True, index=True, nullable=False)
    session_id = Column(String(255), index=True, nullable=False)
    payload_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of AttestationToken."""
        return f"<AttestationToken(id={self.id}, session_id={self.session_id}, expires_at={self.expires_at})>"

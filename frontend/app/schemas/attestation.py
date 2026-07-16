"""
Pydantic schema for attestation token payloads.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class AttestationTokenPayload(BaseModel):
    """
    Schema for attestation token payloads.
    
    Attributes:
        agent_id: Identifier of the requesting agent
        user_role: Role of the user making the request
        target_tables: List of database tables being accessed
        timestamp: When the token was created
        session_id: Session identifier
    """
    
    agent_id: str = Field(..., min_length=1, max_length=255, description="Agent identifier")
    user_role: str = Field(..., min_length=1, max_length=50, description="User role")
    target_tables: List[str] = Field(default_factory=list, description="Database tables being accessed")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Token creation time")
    session_id: str = Field(..., min_length=1, max_length=255, description="Session identifier")
    
    @validator("target_tables")
    def validate_target_tables(cls, v: List[str]) -> List[str]:
        """Validate target tables list."""
        if len(v) > 100:
            raise ValueError("Cannot access more than 100 tables in a single token")
        for table in v:
            if not all(c.isalnum() or c in "_" for c in table):
                raise ValueError(f"Invalid table name: {table}")
        return v
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "agent_id": "Support-Agent-Alpha",
                "user_role": "analyst_l3",
                "target_tables": ["contracts", "invoices"],
                "session_id": "sess_12345",
                "timestamp": "2026-07-16T13:10:04Z"
            }
        }

"""
Pydantic schema for parameterized database queries.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional
import json


class DatabaseQuery(BaseModel):
    """
    Schema for parameterized database queries.
    
    Attributes:
        query: SQL query with placeholders (e.g., SELECT * FROM users WHERE id = :id)
        parameters: Query parameters (e.g., {"id": 123})
        session_id: Session identifier for tracking
        attestation_token: Optional cryptographic attestation token
    """
    
    query: str = Field(..., min_length=1, description="Parameterized SQL query")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Query parameters")
    session_id: str = Field(..., min_length=1, max_length=255, description="Session identifier")
    attestation_token: Optional[str] = Field(
        None,
        description="HMAC-SHA256 attestation token"
    )
    
    @validator("query")
    def validate_query(cls, v: str) -> str:
        """Validate SQL query structure."""
        if not v.strip():
            raise ValueError("Query cannot be empty")
        if len(v) > 10000:
            raise ValueError("Query exceeds maximum length of 10000 characters")
        return v
    
    @validator("parameters")
    def validate_parameters(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate query parameters are JSON-serializable."""
        try:
            json.dumps(v)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Parameters must be JSON-serializable: {e}")
        return v
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "query": "SELECT * FROM users WHERE id = :id",
                "parameters": {"id": 123},
                "session_id": "sess_12345",
                "attestation_token": "token_abc123"
            }
        }

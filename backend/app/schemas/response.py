"""Pydantic schemas for API responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Generic success response wrapper.
    
    Wraps successful operation responses with metadata.
    """

    success: bool = True
    data: Any = Field(..., description="Response data")
    message: Optional[str] = Field(
        default=None,
        description="Optional success message"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": 1, "username": "analyst"},
                "message": "Operation successful",
                "timestamp": "2026-07-16T12:00:00Z",
            }
        }


class ErrorResponse(BaseModel):
    """Generic error response wrapper.
    
    Wraps error responses with detailed information.
    """

    success: bool = False
    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(default=None)
    request_id: Optional[str] = Field(default=None)
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": False,
                "error_code": "VALIDATION_ERROR",
                "message": "Invalid query parameters",
                "details": {"field": "limit", "reason": "exceeds maximum"},
                "request_id": "req_abc123",
                "timestamp": "2026-07-16T12:00:00Z",
            }
        }


class TokenResponse(BaseModel):
    """Response containing an attestation token.
    
    Attributes:
        token: The HMAC token string
        expires_at: When the token expires (UTC)
        ttl_seconds: Time-to-live in seconds
    """

    token: str = Field(..., description="HMAC attestation token")
    expires_at: datetime = Field(..., description="Expiration time")
    ttl_seconds: int = Field(..., description="Token lifetime in seconds")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "token": "token_string_here",
                "expires_at": "2026-07-16T12:00:30Z",
                "ttl_seconds": 30,
            }
        }


class TokenVerificationResult(BaseModel):
    """Result of token verification.
    
    Attributes:
        valid: Whether the token is valid
        expired: Whether the token has expired
        reason: Reason if invalid
        verified_at: When verification occurred
    """

    valid: bool = Field(...)
    expired: bool = Field(default=False)
    reason: Optional[str] = Field(default=None)
    verified_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When verification occurred"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "valid": True,
                "expired": False,
                "verified_at": "2026-07-16T12:00:15Z",
            }
        }


class DatabaseQueryResult(BaseModel):
    """Result of a database query.
    
    Attributes:
        rows: List of result rows
        row_count: Number of rows returned
        columns: Column names in result
        execution_time_ms: Query execution time in milliseconds
        transaction_id: Unique transaction ID for audit
    """

    rows: List[Dict[str, Any]] = Field(default_factory=list)
    row_count: int = Field(default=0)
    columns: List[str] = Field(default_factory=list)
    execution_time_ms: float = Field(default=0.0)
    transaction_id: str = Field(...)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "rows": [
                    {"id": 1, "username": "analyst", "role": "analyst_l3"},
                    {"id": 2, "username": "ops", "role": "ops_team"},
                ],
                "row_count": 2,
                "columns": ["id", "username", "role"],
                "execution_time_ms": 45.2,
                "transaction_id": "txn_abc123",
            }
        }


class ValidationResult(BaseModel):
    """Result of schema validation.
    
    Attributes:
        valid: Whether validation passed
        errors: List of validation errors if any
    """

    valid: bool = Field(...)
    errors: List[str] = Field(default_factory=list)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "valid": False,
                "errors": [
                    "Missing required field: 'query'",
                    "Parameter count mismatch: expected 2, got 1",
                ],
            }
        }

"""Pydantic schemas for incoming API requests."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class ToolCallRequest(BaseModel):
    """Schema for tool call requests from the agent.
    
    This represents a request from an AI agent to execute a tool or query.
    Includes optional attestation token for permission verification.
    
    Attributes:
        tool: Name of the tool being called (e.g., "query_database", "list_tables")
        arguments: Key-value pairs of arguments passed to the tool
        context: Optional context information (user_id, session_id, ticket_id, etc.)
        attestation_token: Optional HMAC token proving authorization
    """

    tool: str = Field(..., min_length=1, max_length=255, description="Tool name")
    arguments: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tool arguments as key-value pairs"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional execution context"
    )
    attestation_token: Optional[str] = Field(
        default=None,
        description="Optional HMAC attestation token"
    )

    @validator("arguments")
    def validate_arguments(cls, v):
        """Validate arguments structure and detect injection patterns."""
        if not isinstance(v, dict):
            raise ValueError("arguments must be a dictionary")
        
        # Check for suspicious patterns in string values
        for key, value in v.items():
            if isinstance(value, str):
                # Check for common injection patterns
                suspicious_patterns = [
                    "'; DROP",
                    "' OR '1'='1",
                    "\" OR \"1\"=\"1",
                    "<script>",
                    "${",
                    "eval(",
                ]
                value_upper = value.upper()
                for pattern in suspicious_patterns:
                    if pattern.upper() in value_upper:
                        raise ValueError(
                            f"Potential injection pattern detected in '{key}': {pattern}"
                        )
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "tool": "query_database",
                "arguments": {
                    "query": "SELECT * FROM users WHERE id = ?",
                    "params": [123],
                    "limit": 10,
                },
                "context": {
                    "user_id": 1,
                    "ticket_id": 42,
                    "session_id": "abc123",
                },
                "attestation_token": "token_string_here",
            }
        }


class DatabaseQueryRequest(BaseModel):
    """Schema for database query requests.
    
    Enforces parameterized queries and validates structure.
    
    Attributes:
        query: SQL query with placeholders (e.g., SELECT * FROM users WHERE id = ?)
        params: List of parameters to bind to query placeholders
        limit: Maximum rows to return (optional, default 100, max 10000)
        timeout_seconds: Query timeout in seconds (optional, default 30)
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Parameterized SQL query"
    )
    params: List[Any] = Field(
        default_factory=list,
        description="Query parameters for placeholders"
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Max rows to return"
    )
    timeout_seconds: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Query timeout"
    )

    @validator("query")
    def validate_query(cls, v):
        """Validate SQL query structure."""
        # Check for raw string injection attempts
        if ";" in v and not v.strip().endswith(";"):
            # Allow semicolon only at end (single statement)
            raise ValueError("Multiple SQL statements not allowed")
        
        # Check for suspicious keywords that suggest non-parameterized queries
        suspicious = ["EXEC ", "EXECUTE ", "DROP ", "DELETE ", "TRUNCATE "]
        v_upper = v.upper()
        for keyword in suspicious:
            if keyword in v_upper:
                raise ValueError(f"Potentially dangerous keyword '{keyword}' not allowed")
        
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "query": "SELECT * FROM users WHERE id = ? AND role = ?",
                "params": [123, "admin"],
                "limit": 100,
                "timeout_seconds": 30,
            }
        }


class TokenMintRequest(BaseModel):
    """Schema for token minting requests.
    
    Attributes:
        agent_id: Identifier of the requesting agent
        user_id: ID of the user making the request
        user_role: Role of the user (admin, analyst_l3, ops_team)
        ticket_id: Optional work ticket ID
        target_tables: Optional list of tables being accessed
        additional_context: Optional extra metadata
    """

    agent_id: str = Field(..., min_length=1, max_length=255)
    user_id: int = Field(..., gt=0)
    user_role: str = Field(..., min_length=1, max_length=50)
    ticket_id: Optional[int] = Field(default=None, gt=0)
    target_tables: Optional[List[str]] = Field(default=None)
    additional_context: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "agent_id": "agent_gpt4_001",
                "user_id": 1,
                "user_role": "analyst_l3",
                "ticket_id": 42,
                "target_tables": ["users", "accounts"],
            }
        }


class TokenVerifyRequest(BaseModel):
    """Schema for token verification requests.
    
    Attributes:
        token: The token string to verify
        expected_session_id: Optional session ID to cross-check
    """

    token: str = Field(..., min_length=1)
    expected_session_id: Optional[str] = Field(default=None)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "token": "token_string_here",
                "expected_session_id": "session_123",
            }
        }


class SchemaValidationRequest(BaseModel):
    """Schema for validating tool calls against expected schemas.
    
    Attributes:
        tool: Tool name to validate against
        arguments: Arguments to validate
    """

    tool: str = Field(..., min_length=1, max_length=255)
    arguments: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "tool": "query_database",
                "arguments": {
                    "query": "SELECT * FROM users",
                    "limit": 100,
                },
            }
        }

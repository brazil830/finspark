"""
Pydantic schema for tool call requests from AI agents.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional
import json


class ToolCallRequest(BaseModel):
    """
    Schema for validated tool call requests from AI agents.
    
    Attributes:
        tool: The name of the tool/function to execute
        arguments: The arguments to pass to the tool
        context_justification_ticket: Optional ticket ID for context
    """
    
    tool: str = Field(..., min_length=1, max_length=255, description="Tool name")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")
    context_justification_ticket: Optional[str] = Field(
        None, 
        max_length=255,
        description="Work ticket providing context for this request"
    )
    
    @validator("tool")
    def validate_tool_name(cls, v: str) -> str:
        """Validate tool name contains only alphanumeric, underscore, and hyphen."""
        if not all(c.isalnum() or c in "_-" for c in v):
            raise ValueError("Tool name must contain only alphanumeric, underscore, or hyphen characters")
        return v
    
    @validator("arguments")
    def validate_arguments_json(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that arguments can be serialized to JSON."""
        try:
            json.dumps(v)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Arguments must be JSON-serializable: {e}")
        return v
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "tool": "read_customer_contracts",
                "arguments": {"limit": 5},
                "context_justification_ticket": "TICKET-123"
            }
        }

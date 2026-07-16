"""Agent execution route handlers."""

import logging
import uuid
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Request

from app.schemas import ToolCallRequest, SuccessResponse, ValidationResult
from app.services import (
    get_schema_validator,
    get_token_validator,
    get_honey_detector,
    get_session_manager,
)

logger = logging.getLogger(__name__)

router_agent = APIRouter(prefix="/agent", tags=["agent"])

# In-memory tracking of active queries (in production, use Redis or database)
_active_queries: Dict[str, Dict[str, Any]] = {}


@router_agent.post("/execute")
async def execute_agent_query(request_body: ToolCallRequest, request: Request):
    """Execute validated agent query.
    
    Validates tool call, checks token, and executes the tool.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
    
    try:
        logger.info(
            f"[{request_id}] Executing agent query: tool={request_body.tool}, "
            f"txn={transaction_id}"
        )
        
        # Validate schema
        validator = get_schema_validator()
        is_valid, errors = validator.validate_tool_call(
            tool=request_body.tool,
            arguments=request_body.arguments,
        )
        
        if not is_valid:
            logger.warning(
                f"[{request_id}] Tool validation failed: {errors}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Tool validation failed: {'; '.join(errors)}"
            )
        
        # Verify attestation token if provided
        if request_body.attestation_token:
            token_validator = get_token_validator()
            token_result = token_validator.verify_token(
                request_body.attestation_token
            )
            
            if not token_result["valid"]:
                logger.warning(
                    f"[{request_id}] Token verification failed: {token_result.get('reason')}"
                )
                raise HTTPException(
                    status_code=401,
                    detail="Invalid attestation token"
                )
            
            logger.info(f"[{request_id}] Token verified for session={token_result['session_id']}")
        
        # Execute tool (mock implementation)
        result = {
            "status": "executed",
            "data": {
                "tool": request_body.tool,
                "arguments_count": len(request_body.arguments),
                "result_preview": "Query executed successfully",
            },
        }
        
        logger.info(
            f"[{request_id}] Agent query executed: tool={request_body.tool}, "
            f"txn={transaction_id}"
        )
        
        return SuccessResponse(
            data={
                "transaction_id": transaction_id,
                "tool": request_body.tool,
                "status": "executed",
                "result": result,
            },
            message="Agent query executed successfully",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"[{request_id}] Agent query execution failed: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Agent query execution failed"
        )


@router_agent.post("/validate")
async def validate_query(request_body: ToolCallRequest, request: Request):
    """Pre-validate query without execution.
    
    Validates tool schema and structure without executing.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        logger.info(
            f"[{request_id}] Validating agent query: tool={request_body.tool}"
        )
        
        validator = get_schema_validator()
        is_valid, errors = validator.validate_tool_call(
            tool=request_body.tool,
            arguments=request_body.arguments,
        )
        
        if is_valid:
            logger.info(f"[{request_id}] Query validation passed")
        else:
            logger.warning(f"[{request_id}] Query validation failed: {errors}")
        
        return SuccessResponse(
            data=ValidationResult(
                valid=is_valid,
                errors=errors,
            ).dict(),
            message="Query validation completed",
        )
    
    except Exception as e:
        logger.error(
            f"[{request_id}] Query validation failed: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Query validation failed"
        )


@router_agent.get("/status")
async def get_agent_status(request: Request):
    """Get current agent status.
    
    Returns status and statistics about agent operations.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        active_count = len(_active_queries)
        
        return SuccessResponse(
            data={
                "status": "ready",
                "active_queries": active_count,
                "timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
            },
            message="Agent status retrieved",
        )
    
    except Exception as e:
        logger.error(
            f"[{request_id}] Failed to get agent status: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to get agent status"
        )

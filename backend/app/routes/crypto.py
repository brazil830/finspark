"""Cryptographic token management route handlers."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request

from app.schemas import TokenMintRequest, TokenVerifyRequest, SuccessResponse
from app.services import (
    get_token_minter,
    get_token_validator,
    get_hsm_manager,
    Permission,
    get_access_control,
)

logger = logging.getLogger(__name__)

router_crypto = APIRouter(prefix="/crypto", tags=["crypto"])


@router_crypto.post("/mint-token")
async def mint_token(request_body: TokenMintRequest, request: Request):
    """Mint a new attestation token.
    
    Creates an HMAC-SHA256 signed token for the requesting agent.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        logger.info(
            f"[{request_id}] Minting token for agent={request_body.agent_id}, "
            f"user={request_body.user_id}"
        )
        
        minter = get_token_minter()
        
        payload = {}
        if request_body.ticket_id:
            payload["ticket_id"] = request_body.ticket_id
        if request_body.target_tables:
            payload["target_tables"] = request_body.target_tables
        if request_body.additional_context:
            payload.update(request_body.additional_context)
        
        mint_result = minter.mint_token(
            agent_id=request_body.agent_id,
            user_id=request_body.user_id,
            user_role=request_body.user_role,
            payload=payload,
        )
        
        logger.info(f"[{request_id}] Token minted for agent={request_body.agent_id}")
        
        return SuccessResponse(
            data={
                "token": mint_result["token"],
                "expires_at": mint_result["expires_at"],
                "ttl_seconds": mint_result["ttl_seconds"],
            },
            message="Token minted successfully",
        )
    
    except ValueError as e:
        logger.warning(f"[{request_id}] Token minting validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"[{request_id}] Token minting failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Token minting failed")


@router_crypto.post("/verify-token")
async def verify_token(request_body: TokenVerifyRequest, request: Request):
    """Verify an attestation token."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        logger.info(f"[{request_id}] Verifying token")
        
        validator = get_token_validator()
        
        result = validator.verify_token(
            request_body.token,
            expected_session_id=request_body.expected_session_id,
        )
        
        if not result["valid"]:
            logger.warning(
                f"[{request_id}] Token verification failed: {result.get('reason')}"
            )
        else:
            logger.info(f"[{request_id}] Token verified successfully")
        
        return SuccessResponse(
            data={
                "valid": result["valid"],
                "expired": result["expired"],
                "reason": result.get("reason"),
                "verified_at": result["verified_at"],
            },
            message="Token verification completed",
        )
    
    except Exception as e:
        logger.error(f"[{request_id}] Token verification failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Token verification failed")


@router_crypto.post("/rotate-hsm")
async def rotate_hsm_key(request: Request):
    """Rotate HSM key (requires admin role)."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        session = getattr(request.state, "session", None)
        if not session:
            logger.warning(f"[{request_id}] HSM rotation without session")
            raise HTTPException(status_code=401, detail="Authentication required")
        
        access_control = get_access_control()
        if not access_control.has_permission(session.role, Permission.ROTATE_HSM_KEYS):
            logger.warning(f"[{request_id}] Unauthorized HSM rotation by user={session.user_id}")
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        logger.info(f"[{request_id}] Rotating HSM key")
        
        hsm_manager = get_hsm_manager()
        if hsm_manager.should_rotate():
            hsm_manager.rotate_key()
            logger.info(f"[{request_id}] HSM key rotated")
        
        key_id = hsm_manager.get_current_key_id()
        key_age = hsm_manager.get_key_age_minutes()
        
        return SuccessResponse(
            data={
                "rotated": True,
                "new_key_id": key_id,
                "key_age_minutes": round(key_age, 2),
            },
            message="HSM key rotated successfully",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] HSM rotation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="HSM rotation failed")


@router_crypto.get("/key-status")
async def get_key_status(request: Request):
    """Get current HSM key status."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    try:
        hsm_manager = get_hsm_manager()
        
        key_id = hsm_manager.get_current_key_id()
        key_age_minutes = hsm_manager.get_key_age_minutes()
        should_rotate = hsm_manager.should_rotate()
        
        logger.info(
            f"[{request_id}] Key status: id={key_id}, "
            f"age={key_age_minutes:.2f}min, rotate={should_rotate}"
        )
        
        return SuccessResponse(
            data={
                "key_id": key_id,
                "key_age_minutes": round(key_age_minutes, 2),
                "should_rotate": should_rotate,
                "rotation_interval_minutes": 5,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            message="Key status retrieved",
        )
    
    except Exception as e:
        logger.error(f"[{request_id}] Failed to get key status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get key status")

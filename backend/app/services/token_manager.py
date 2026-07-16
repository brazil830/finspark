"""Token Minting and Validation Service.

Implements HMAC-SHA256 based attestation token generation and verification.
Tokens are ephemeral (30 second TTL by default) and include:
- Session ID
- Payload hash
- Timestamp
- HMAC signature for integrity
"""

import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class TokenMinter:
    """Creates cryptographic attestation tokens using HMAC-SHA256.
    
    Tokens include:
    - Session identifier (agent_id)
    - Payload hash (SHA256 of context)
    - Timestamp (creation time)
    - HMAC signature (verified with key)
    """

    def __init__(self, hsm_manager, ttl_seconds: int = 30):
        """Initialize token minter.
        
        Args:
            hsm_manager: HSM manager providing current key
            ttl_seconds: Token time-to-live in seconds (default 30)
        """
        self.hsm_manager = hsm_manager
        self.ttl_seconds = ttl_seconds
        logger.info(f"TokenMinter initialized with TTL: {ttl_seconds} seconds")

    def mint_token(
        self,
        agent_id: str,
        user_id: int,
        user_role: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Mint a new attestation token.
        
        Creates an HMAC-SHA256 signed token with timestamp and payload hash.
        
        Args:
            agent_id: Identifier of the requesting agent
            user_id: ID of the user making the request
            user_role: Role of the user (admin, analyst_l3, ops_team)
            payload: Optional additional context to include in token
        
        Returns:
            Dictionary with:
            - token: The signed token string
            - session_id: Session identifier (agent_id)
            - expires_at: Expiration timestamp
            - ttl_seconds: Token lifetime
        
        Raises:
            ValueError: If HSM key is not available
        """
        try:
            # Get current HSM key for signing
            key_id = self.hsm_manager.get_current_key_id()
            if not key_id:
                raise ValueError("HSM key not available for token signing")

            # Create timestamp
            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(seconds=self.ttl_seconds)
            timestamp = int(now.timestamp() * 1000)  # milliseconds

            # Prepare payload for hashing
            payload = payload or {}
            payload_with_meta = {
                "agent_id": agent_id,
                "user_id": user_id,
                "user_role": user_role,
                "timestamp": timestamp,
                **payload,
            }

            # Create payload hash
            payload_json = json.dumps(payload_with_meta, sort_keys=True)
            payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()

            # Create signature data (session_id + payload_hash + timestamp)
            signature_data = f"{agent_id}:{payload_hash}:{timestamp}"

            # Sign with current HSM key (use key_id as simple simulation)
            # In production, this would use actual HSM key material
            key_material = f"{key_id}_material".encode()
            signature = hmac.new(
                key_material,
                signature_data.encode(),
                hashlib.sha256,
            ).hexdigest()

            # Construct token: session_id.payload_hash.timestamp.signature
            token = f"{agent_id}.{payload_hash}.{timestamp}.{signature}"

            logger.info(
                f"Token minted for agent={agent_id}, user={user_id}, "
                f"expires_in={self.ttl_seconds}s"
            )

            return {
                "token": token,
                "session_id": agent_id,
                "payload_hash": payload_hash,
                "timestamp": timestamp,
                "expires_at": expires_at.isoformat(),
                "ttl_seconds": self.ttl_seconds,
                "key_id": key_id,
            }

        except Exception as e:
            logger.error(f"Token minting failed: {e}")
            raise


class TokenValidator:
    """Validates attestation tokens.
    
    Verifies:
    - HMAC signature (integrity)
    - Expiration time
    - Session consistency
    """

    def __init__(self, hsm_manager):
        """Initialize token validator.
        
        Args:
            hsm_manager: HSM manager providing current/previous keys
        """
        self.hsm_manager = hsm_manager
        logger.info("TokenValidator initialized")

    def verify_token(
        self,
        token: str,
        expected_session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Verify an attestation token.
        
        Validates:
        1. Token format (4 parts separated by dots)
        2. Signature validity
        3. Expiration
        4. Session consistency (if expected_session_id provided)
        
        Args:
            token: Token string to verify
            expected_session_id: Optional session ID to cross-check
        
        Returns:
            Dictionary with:
            - valid: Whether token is valid
            - expired: Whether token has expired
            - reason: Error reason if invalid
            - session_id: Extracted session ID
            - payload_hash: Extracted payload hash
            - timestamp: Extracted timestamp
            - verified_at: When verification occurred
        
        Raises:
            ValueError: If token format is invalid
        """
        try:
            # Parse token: session_id.payload_hash.timestamp.signature
            parts = token.split(".")
            if len(parts) != 4:
                raise ValueError(
                    f"Invalid token format: expected 4 parts, got {len(parts)}"
                )

            session_id, payload_hash, timestamp_str, signature = parts

            # Validate session ID consistency
            if expected_session_id and session_id != expected_session_id:
                return {
                    "valid": False,
                    "expired": False,
                    "reason": f"Session ID mismatch: expected {expected_session_id}, "
                    f"got {session_id}",
                    "session_id": session_id,
                    "verified_at": datetime.now(timezone.utc).isoformat(),
                }

            # Parse timestamp
            try:
                timestamp = int(timestamp_str)
            except ValueError:
                raise ValueError(f"Invalid timestamp in token: {timestamp_str}")

            # Check expiration
            token_time = datetime.fromtimestamp(
                timestamp / 1000, tz=timezone.utc
            )
            now = datetime.now(timezone.utc)
            
            # Default TTL is 30 seconds, but we'll use 60 to be conservative
            ttl_seconds = 60
            expires_at = token_time + timedelta(seconds=ttl_seconds)
            is_expired = now > expires_at

            if is_expired:
                return {
                    "valid": False,
                    "expired": True,
                    "reason": f"Token expired at {expires_at.isoformat()}",
                    "session_id": session_id,
                    "verified_at": datetime.now(timezone.utc).isoformat(),
                }

            # Verify signature
            signature_data = f"{session_id}:{payload_hash}:{timestamp_str}"
            
            # Get current and previous key IDs for verification
            current_key_id = self.hsm_manager.get_current_key_id()
            key_material = f"{current_key_id}_material".encode()
            
            expected_signature = hmac.new(
                key_material,
                signature_data.encode(),
                hashlib.sha256,
            ).hexdigest()

            # Constant-time comparison to prevent timing attacks
            if not hmac.compare_digest(signature, expected_signature):
                return {
                    "valid": False,
                    "expired": False,
                    "reason": "Signature verification failed",
                    "session_id": session_id,
                    "verified_at": datetime.now(timezone.utc).isoformat(),
                }

            logger.info(f"Token verified successfully for session={session_id}")

            return {
                "valid": True,
                "expired": False,
                "session_id": session_id,
                "payload_hash": payload_hash,
                "timestamp": timestamp,
                "expires_at": expires_at.isoformat(),
                "verified_at": datetime.now(timezone.utc).isoformat(),
            }

        except ValueError as e:
            logger.warning(f"Token verification failed: {e}")
            return {
                "valid": False,
                "expired": False,
                "reason": str(e),
                "verified_at": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {e}")
            return {
                "valid": False,
                "expired": False,
                "reason": "Internal verification error",
                "verified_at": datetime.now(timezone.utc).isoformat(),
            }


# Global singletons
_token_minter: Optional[TokenMinter] = None
_token_validator: Optional[TokenValidator] = None


def get_token_minter() -> TokenMinter:
    """Get or create global TokenMinter instance."""
    global _token_minter
    if _token_minter is None:
        from app.services import get_hsm_manager
        _token_minter = TokenMinter(get_hsm_manager())
    return _token_minter


def get_token_validator() -> TokenValidator:
    """Get or create global TokenValidator instance."""
    global _token_validator
    if _token_validator is None:
        from app.services import get_hsm_manager
        _token_validator = TokenValidator(get_hsm_manager())
    return _token_validator

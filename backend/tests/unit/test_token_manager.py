"""Unit tests for token manager (minting and validation)."""

import hashlib
import hmac
import time
from datetime import datetime, timedelta, timezone

import pytest

from app.services.token_manager import TokenMinter, TokenValidator
from app.services.hsm import HSMKeyManager


@pytest.fixture
def hsm_manager():
    """Create HSM manager instance."""
    manager = HSMKeyManager(enable_simulation=True)
    manager.initialize()
    return manager


@pytest.fixture
def token_minter(hsm_manager):
    """Create token minter instance."""
    return TokenMinter(hsm_manager, ttl_seconds=30)


@pytest.fixture
def token_validator(hsm_manager):
    """Create token validator instance."""
    return TokenValidator(hsm_manager)


class TestTokenMinter:
    """Test TokenMinter class."""

    def test_mint_token_success(self, token_minter):
        """Test successful token minting."""
        result = token_minter.mint_token(
            agent_id="agent_001",
            user_id=1,
            user_role="analyst_l3",
        )

        assert "token" in result
        assert "session_id" in result
        assert "expires_at" in result
        assert "ttl_seconds" in result
        assert result["session_id"] == "agent_001"
        assert result["ttl_seconds"] == 30

    def test_mint_token_with_payload(self, token_minter):
        """Test token minting with additional payload."""
        result = token_minter.mint_token(
            agent_id="agent_002",
            user_id=2,
            user_role="admin",
            payload={"ticket_id": 42, "tables": ["users", "accounts"]},
        )

        assert "token" in result
        assert result["session_id"] == "agent_002"
        assert "payload_hash" in result

    def test_token_format(self, token_minter):
        """Test that token has correct format (4 parts)."""
        result = token_minter.mint_token(
            agent_id="agent_003",
            user_id=3,
            user_role="ops_team",
        )

        token = result["token"]
        parts = token.split(".")
        assert len(parts) == 4, "Token should have 4 parts separated by dots"
        assert parts[0] == "agent_003"  # session_id

    def test_token_expires_correctly(self, token_minter):
        """Test that token expiration time is calculated correctly."""
        now = datetime.now(timezone.utc)
        result = token_minter.mint_token(
            agent_id="agent_004",
            user_id=4,
            user_role="analyst_l3",
        )

        expires_at = datetime.fromisoformat(result["expires_at"])
        time_diff = (expires_at - now).total_seconds()

        # Should be approximately 30 seconds
        assert 29 <= time_diff <= 31


class TestTokenValidator:
    """Test TokenValidator class."""

    def test_verify_valid_token(self, token_minter, token_validator):
        """Test verification of a valid token."""
        mint_result = token_minter.mint_token(
            agent_id="agent_005",
            user_id=5,
            user_role="analyst_l3",
        )

        verify_result = token_validator.verify_token(mint_result["token"])

        assert verify_result["valid"] is True
        assert verify_result["expired"] is False
        assert verify_result["session_id"] == "agent_005"

    def test_verify_token_with_session_id(self, token_minter, token_validator):
        """Test token verification with session ID validation."""
        mint_result = token_minter.mint_token(
            agent_id="agent_006",
            user_id=6,
            user_role="analyst_l3",
        )

        verify_result = token_validator.verify_token(
            mint_result["token"],
            expected_session_id="agent_006",
        )

        assert verify_result["valid"] is True

    def test_verify_token_wrong_session_id(self, token_minter, token_validator):
        """Test token verification fails with wrong session ID."""
        mint_result = token_minter.mint_token(
            agent_id="agent_007",
            user_id=7,
            user_role="analyst_l3",
        )

        verify_result = token_validator.verify_token(
            mint_result["token"],
            expected_session_id="agent_wrong",
        )

        assert verify_result["valid"] is False
        assert "Session ID mismatch" in verify_result["reason"]

    def test_verify_invalid_token_format(self, token_validator):
        """Test verification fails with invalid token format."""
        verify_result = token_validator.verify_token("invalid_token")

        assert verify_result["valid"] is False
        assert "format" in verify_result["reason"].lower()

    def test_verify_expired_token(self, hsm_manager, token_validator):
        """Test verification fails with expired token."""
        # Create a minter with very short TTL
        minter = TokenMinter(hsm_manager, ttl_seconds=1)
        mint_result = minter.mint_token(
            agent_id="agent_008",
            user_id=8,
            user_role="analyst_l3",
        )

        # Wait for token to expire (validator uses 60 second buffer, so we need to test differently)
        # Instead, we'll manually construct an old token
        import hashlib
        import hmac
        
        # Create a token from the past
        old_timestamp = int((time.time() - 120) * 1000)  # 2 minutes ago
        session_id = "agent_008"
        payload_hash = "old_hash"
        signature_data = f"{session_id}:{payload_hash}:{old_timestamp}"
        
        key_id = hsm_manager.get_current_key_id()
        key_material = f"{key_id}_material".encode()
        signature = hmac.new(
            key_material,
            signature_data.encode(),
            hashlib.sha256,
        ).hexdigest()
        
        old_token = f"{session_id}.{payload_hash}.{old_timestamp}.{signature}"
        
        verify_result = token_validator.verify_token(old_token)

        assert verify_result["valid"] is False
        assert verify_result["expired"] is True

    def test_verify_token_tampered_signature(self, token_minter, token_validator):
        """Test verification fails with tampered signature."""
        mint_result = token_minter.mint_token(
            agent_id="agent_009",
            user_id=9,
            user_role="analyst_l3",
        )

        # Tamper with the token
        token = mint_result["token"]
        parts = token.split(".")
        # Change last character of signature
        tampered_signature = parts[3][:-1] + ("0" if parts[3][-1] != "0" else "1")
        tampered_token = ".".join(parts[:-1] + [tampered_signature])

        verify_result = token_validator.verify_token(tampered_token)

        assert verify_result["valid"] is False
        assert "signature" in verify_result["reason"].lower()

    def test_verify_token_missing_parts(self, token_validator):
        """Test verification fails with incomplete token."""
        verify_result = token_validator.verify_token("agent_001.hash.timestamp")

        assert verify_result["valid"] is False
        assert "format" in verify_result["reason"].lower()

    def test_token_roundtrip(self, token_minter, token_validator):
        """Test complete token minting and verification cycle."""
        # Mint token
        mint_result = token_minter.mint_token(
            agent_id="agent_010",
            user_id=10,
            user_role="admin",
            payload={"ticket_id": 100},
        )

        # Verify token
        verify_result = token_validator.verify_token(
            mint_result["token"],
            expected_session_id="agent_010",
        )

        assert verify_result["valid"] is True
        assert verify_result["session_id"] == "agent_010"
        assert verify_result["payload_hash"] == mint_result["payload_hash"]

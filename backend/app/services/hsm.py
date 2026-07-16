"""HSM (Hardware Security Module) key management service."""

import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


class HSMKeyManager:
    """Manages HSM keys and rotation."""

    def __init__(self, enable_simulation: bool = True):
        """Initialize HSM key manager.

        Args:
            enable_simulation: If True, simulate HSM without actual hardware
        """
        self.enable_simulation = enable_simulation
        self.current_key_id: Optional[str] = None
        self.key_created_at: float = 0
        self.rotation_interval_seconds: int = 300  # 5 minutes default

    def initialize(self):
        """Initialize HSM and load or create initial key."""
        try:
            self.current_key_id = "key_initial"
            self.key_created_at = time.time()
            logger.info(
                f"HSM initialized with key: {self.current_key_id}",
                extra={"key_id": self.current_key_id},
            )
        except Exception as e:
            logger.error(f"HSM initialization failed: {e}")
            raise

    def get_current_key_id(self) -> str:
        """Get current active key ID."""
        return self.current_key_id or "key_unknown"

    def get_key_age_minutes(self) -> float:
        """Get age of current key in minutes."""
        if not self.key_created_at:
            return 0
        return (time.time() - self.key_created_at) / 60

    def should_rotate(self) -> bool:
        """Check if key should be rotated."""
        age_seconds = time.time() - self.key_created_at
        return age_seconds > self.rotation_interval_seconds

    def rotate_key(self) -> str:
        """Rotate HSM key.

        Returns:
            New key ID
        """
        try:
            old_key_id = self.current_key_id
            # Generate new key ID based on timestamp
            new_key_id = f"key_{int(time.time())}"
            self.current_key_id = new_key_id
            self.key_created_at = time.time()

            logger.info(
                f"HSM key rotated: {old_key_id} -> {new_key_id}",
                extra={
                    "old_key_id": old_key_id,
                    "new_key_id": new_key_id,
                },
            )

            return new_key_id
        except Exception as e:
            logger.error(f"HSM key rotation failed: {e}")
            raise

    def get_status(self) -> dict:
        """Get HSM status information."""
        return {
            "current_key_id": self.get_current_key_id(),
            "key_age_minutes": round(self.get_key_age_minutes(), 2),
            "next_rotation_at": int(self.key_created_at + self.rotation_interval_seconds),
            "simulation_enabled": self.enable_simulation,
        }


# Global HSM manager instance
_hsm_manager = HSMKeyManager()


def get_hsm_manager() -> HSMKeyManager:
    """Get the global HSM manager instance."""
    return _hsm_manager

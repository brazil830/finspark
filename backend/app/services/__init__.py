"""Application services."""

from app.services.database import DatabaseManager, get_db_manager
from app.services.honey_detector import HoneyTableDetector, get_honey_detector
from app.services.hsm import HSMKeyManager, get_hsm_manager
from app.services.jwt_manager import JWTManager, get_jwt_manager
from app.services.token_manager import TokenMinter, TokenValidator, get_token_minter, get_token_validator
from app.services.schema_validator import SchemaValidator, get_schema_validator
from app.services.access_control import (
    RoleBasedAccessControl,
    SessionContext,
    SessionManager,
    UserRole,
    Permission,
    get_access_control,
    get_session_manager,
)

__all__ = [
    # Database services
    "DatabaseManager",
    "get_db_manager",
    # HSM services
    "HSMKeyManager",
    "get_hsm_manager",
    # Honey detection
    "HoneyTableDetector",
    "get_honey_detector",
    # JWT services
    "JWTManager",
    "get_jwt_manager",
    # Token management
    "TokenMinter",
    "TokenValidator",
    "get_token_minter",
    "get_token_validator",
    # Schema validation
    "SchemaValidator",
    "get_schema_validator",
    # Access control
    "RoleBasedAccessControl",
    "SessionContext",
    "SessionManager",
    "UserRole",
    "Permission",
    "get_access_control",
    "get_session_manager",
]

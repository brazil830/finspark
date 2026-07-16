"""JWT Token Management Service.

Implements JWT-based authentication with:
- Token generation (access and refresh tokens)
- Token validation and claims verification
- Password hashing with bcrypt
- User session management
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTManager:
    """Manages JWT token generation and validation."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
    ):
        """Initialize JWT manager.

        Args:
            secret_key: Secret key for signing tokens
            algorithm: JWT algorithm (default HS256)
            access_token_expire_minutes: Access token TTL in minutes
            refresh_token_expire_days: Refresh token TTL in days
        """
        if not secret_key or secret_key == "your-secret-key-change-in-production":
            logger.warning("JWT Secret key is not set or is default - SECURITY RISK")
        
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        logger.info(
            f"JWTManager initialized with algorithm={algorithm}, "
            f"access_token_ttl={access_token_expire_minutes}min"
        )

    def create_access_token(
        self,
        subject: str,
        user_id: int,
        role: str,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create an access token.

        Args:
            subject: Token subject (typically username or user_id)
            user_id: ID of the user
            role: User role (admin, analyst_l3, ops_team)
            additional_claims: Optional additional claims to include

        Returns:
            Dictionary with:
            - access_token: JWT token string
            - token_type: Token type (Bearer)
            - expires_in: Expiration time in seconds
            - expires_at: Expiration timestamp
        """
        try:
            now = datetime.now(timezone.utc)
            expires = now + timedelta(minutes=self.access_token_expire_minutes)

            claims = {
                "sub": subject,
                "user_id": user_id,
                "role": role,
                "type": "access",
                "iat": now,
                "exp": expires,
            }

            if additional_claims:
                claims.update(additional_claims)

            token = jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

            expires_in = int(self.access_token_expire_minutes * 60)

            logger.info(
                f"Access token created for user_id={user_id}, role={role}, "
                f"expires_in={expires_in}s"
            )

            return {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": expires_in,
                "expires_at": expires.isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise

    def create_refresh_token(
        self,
        subject: str,
        user_id: int,
    ) -> Dict[str, Any]:
        """Create a refresh token.

        Args:
            subject: Token subject (typically username or user_id)
            user_id: ID of the user

        Returns:
            Dictionary with:
            - refresh_token: JWT token string
            - token_type: Token type (Bearer)
            - expires_in: Expiration time in seconds
            - expires_at: Expiration timestamp
        """
        try:
            now = datetime.now(timezone.utc)
            expires = now + timedelta(days=self.refresh_token_expire_days)

            claims = {
                "sub": subject,
                "user_id": user_id,
                "type": "refresh",
                "iat": now,
                "exp": expires,
            }

            token = jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

            expires_in = int(self.refresh_token_expire_days * 24 * 60 * 60)

            logger.info(
                f"Refresh token created for user_id={user_id}, "
                f"expires_in={expires_in}s"
            )

            return {
                "refresh_token": token,
                "token_type": "Bearer",
                "expires_in": expires_in,
                "expires_at": expires.isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to create refresh token: {e}")
            raise

    def verify_token(
        self,
        token: str,
        token_type: str = "access",
    ) -> Dict[str, Any]:
        """Verify and decode a JWT token.

        Args:
            token: JWT token string to verify
            token_type: Expected token type (access or refresh)

        Returns:
            Dictionary with decoded claims if valid

        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Verify token type
            if payload.get("type") != token_type:
                raise jwt.InvalidTokenError(
                    f"Invalid token type: expected {token_type}, "
                    f"got {payload.get('type')}"
                )

            logger.info(f"Token verified successfully for user_id={payload.get('user_id')}")

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning(f"Token has expired")
            raise

        except jwt.InvalidTokenError as e:
            logger.warning(f"Token verification failed: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during token verification: {e}")
            raise

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to check against

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)


# Global singleton
_jwt_manager: Optional[JWTManager] = None


def get_jwt_manager() -> JWTManager:
    """Get or create global JWTManager instance."""
    global _jwt_manager
    if _jwt_manager is None:
        from app.config.settings import settings
        _jwt_manager = JWTManager(
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
            access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    return _jwt_manager

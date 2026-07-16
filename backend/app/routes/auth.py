"""Authentication routes for user registration, login, and token management.

Endpoints:
    POST /auth/register - Register a new user
    POST /auth/login - Login with credentials
    POST /auth/refresh - Refresh access token
    POST /auth/logout - Logout user
    GET /auth/me - Get current user profile
    POST /auth/change-password - Change password
"""

import logging
from datetime import datetime, timezone
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.models.user import User, UserRole
from app.schemas.auth import (
    ChangePasswordRequest,
    ErrorResponse,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    RefreshTokenRequest,
    RegistrationResponse,
    TokenResponse,
    UserProfile,
    UserResponse,
    RegisterRequest,
)
from database.engine import PostgresSessionFactory
from app.services.jwt_manager import JWTManager, get_jwt_manager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        409: {"model": ErrorResponse, "description": "Conflict"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)


# ============================================================================
# Dependency Functions
# ============================================================================


async def get_current_user(
    request: Request,
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> dict:
    """Get current authenticated user from JWT token.

    Args:
        request: FastAPI Request object
        jwt_manager: JWT manager instance

    Returns:
        Decoded JWT claims

    Raises:
        HTTPException: If token is missing, invalid, or expired
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Parse Bearer token
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify token
    try:
        claims = jwt_manager.verify_token(token, token_type="access")
        return claims
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================================
# Endpoints
# ============================================================================


@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User successfully registered"},
        409: {"description": "Username or email already exists"},
        400: {"description": "Invalid input"},
    },
)
async def register(
    request: RegisterRequest,
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> RegistrationResponse:
    """Register a new user account.

    Args:
        request: Registration request with username, email, password

    Returns:
        RegistrationResponse with created user

    Raises:
        HTTPException: If username or email already exists or validation fails
    """
    try:
        # Check if user already exists
        async with PostgresSessionFactory() as session:
            # Check username uniqueness
            existing = await session.execute(
                select(User).where(User.username == request.username)
            )
            if existing.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists",
                )

            # Check email uniqueness
            existing = await session.execute(
                select(User).where(User.email == request.email)
            )
            if existing.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )

            # Hash password
            password_hash = jwt_manager.hash_password(request.password)

            # Create new user
            new_user = User(
                username=request.username,
                email=request.email,
                password_hash=password_hash,
                full_name=request.full_name,
                role=UserRole.OPS_TEAM,  # Default role for new users
                is_active=True,
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            logger.info(f"User registered: {new_user.username}")

            # Return success response
            return RegistrationResponse(
                user=UserResponse(
                    id=new_user.id,
                    username=new_user.username,
                    email=new_user.email,
                    role=new_user.role.value,
                    full_name=new_user.full_name,
                    is_active=new_user.is_active,
                    created_at=new_user.created_at.isoformat(),
                ),
                message="User registered successfully",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login with credentials",
    responses={
        200: {"description": "Successfully logged in"},
        401: {"description": "Invalid credentials"},
        400: {"description": "User inactive"},
    },
)
async def login(
    request: LoginRequest,
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> LoginResponse:
    """Login with username and password.

    Args:
        request: Login request with username and password

    Returns:
        LoginResponse with user info and tokens

    Raises:
        HTTPException: If credentials invalid or user inactive
    """
    try:
        async with PostgresSessionFactory() as session:
            # Find user by username
            result = await session.execute(
                select(User).where(User.username == request.username)
            )
            user = result.scalars().first()

            if not user:
                logger.warning(f"Login failed: user not found - {request.username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

            # Check if user is active
            if not user.is_active:
                logger.warning(f"Login failed: user inactive - {request.username}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User account is inactive",
                )

            # Verify password
            if not jwt_manager.verify_password(request.password, user.password_hash):
                logger.warning(f"Login failed: invalid password - {request.username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

            # Update last_login timestamp
            user.last_login = datetime.now(timezone.utc)
            session.add(user)
            await session.commit()

            logger.info(f"User logged in: {user.username}")

            # Create tokens
            access_token_data = jwt_manager.create_access_token(
                subject=user.username,
                user_id=user.id,
                role=user.role.value,
            )
            refresh_token_data = jwt_manager.create_refresh_token(
                subject=user.username,
                user_id=user.id,
            )

            return LoginResponse(
                user=UserProfile(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    role=user.role.value,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    created_at=user.created_at.isoformat(),
                    last_login=user.last_login.isoformat() if user.last_login else None,
                ),
                access_token=access_token_data["access_token"],
                refresh_token=refresh_token_data["refresh_token"],
                token_type=access_token_data["token_type"],
                expires_in=access_token_data["expires_in"],
                expires_at=access_token_data["expires_at"],
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    responses={
        200: {"description": "Access token refreshed"},
        401: {"description": "Invalid or expired refresh token"},
    },
)
async def refresh_token(
    request: RefreshTokenRequest,
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> TokenResponse:
    """Refresh access token using refresh token.

    Args:
        request: Refresh token request

    Returns:
        TokenResponse with new access token

    Raises:
        HTTPException: If refresh token invalid or expired
    """
    try:
        # Verify refresh token
        claims = jwt_manager.verify_token(request.refresh_token, token_type="refresh")

        # Create new access token
        access_token_data = jwt_manager.create_access_token(
            subject=claims["sub"],
            user_id=claims["user_id"],
            role="user",  # Default role - could be retrieved from DB
        )

        logger.info(f"Token refreshed for user_id={claims['user_id']}")

        return TokenResponse(
            access_token=access_token_data["access_token"],
            token_type=access_token_data["token_type"],
            expires_in=access_token_data["expires_in"],
            expires_at=access_token_data["expires_at"],
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed",
        )


@router.get(
    "/me",
    response_model=UserProfile,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
)
async def get_current_user_profile(
    claims: dict = Depends(get_current_user),
) -> UserProfile:
    """Get current authenticated user profile.

    Args:
        claims: JWT claims from current user

    Returns:
        UserProfile with user information

    Raises:
        HTTPException: If user not found
    """
    try:
        async with PostgresSessionFactory() as session:
            user = await session.get(User, claims["user_id"])
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            return UserProfile(
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role.value,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at.isoformat(),
                last_login=user.last_login.isoformat() if user.last_login else None,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile",
        )


@router.post(
    "/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Change user password",
)
async def change_password(
    request: ChangePasswordRequest,
    claims: dict = Depends(get_current_user),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> MessageResponse:
    """Change current user password.

    Args:
        request: Change password request with current and new password
        claims: JWT claims from current user

    Returns:
        MessageResponse with success message

    Raises:
        HTTPException: If current password invalid or validation fails
    """
    try:
        async with PostgresSessionFactory() as session:
            user = await session.get(User, claims["user_id"])
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            # Verify current password
            if not jwt_manager.verify_password(request.current_password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Current password is incorrect",
                )

            # Hash and update new password
            user.password_hash = jwt_manager.hash_password(request.new_password)
            session.add(user)
            await session.commit()

            logger.info(f"Password changed for user: {user.username}")

            return MessageResponse(message="Password changed successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed",
        )


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
)
async def logout(
    claims: dict = Depends(get_current_user),
) -> MessageResponse:
    """Logout current user.

    Note: Token is not invalidated server-side. Client should discard token.
    With stateless JWT, token remains valid until expiry.

    Args:
        claims: JWT claims from current user

    Returns:
        MessageResponse with logout confirmation
    """
    logger.info(f"User logged out: user_id={claims['user_id']}")
    return MessageResponse(
        message="Logged out successfully",
        detail="Token remains valid until expiry. Please discard locally.",
    )

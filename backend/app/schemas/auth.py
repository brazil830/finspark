"""Authentication request and response schemas.

Includes:
- User registration
- User login
- Token responses
- User profile
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# Request Schemas
# ============================================================================


class RegisterRequest(BaseModel):
    """User registration request."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePassword123!",
                "full_name": "John Doe",
            }
        }


class LoginRequest(BaseModel):
    """User login request."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "SecurePassword123!",
            }
        }


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }


class ChangePasswordRequest(BaseModel):
    """Password change request."""

    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "CurrentPassword123!",
                "new_password": "NewPassword456!",
            }
        }


# ============================================================================
# Response Schemas
# ============================================================================


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    expires_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 1800,
                "expires_at": "2026-07-16T14:30:00Z",
            }
        }


class UserProfile(BaseModel):
    """User profile response."""

    id: int
    username: str
    email: str
    role: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: str
    last_login: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "role": "analyst_l3",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2026-07-16T10:00:00Z",
                "last_login": "2026-07-16T14:00:00Z",
            }
        }


class UserResponse(BaseModel):
    """Standard user response."""

    id: int
    username: str
    email: str
    role: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "role": "analyst_l3",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2026-07-16T10:00:00Z",
            }
        }


class LoginResponse(BaseModel):
    """Login response with user and tokens."""

    user: UserProfile
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    expires_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "role": "analyst_l3",
                    "full_name": "John Doe",
                    "is_active": True,
                    "created_at": "2026-07-16T10:00:00Z",
                    "last_login": "2026-07-16T14:00:00Z",
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 1800,
                "expires_at": "2026-07-16T14:30:00Z",
            }
        }


class RegistrationResponse(BaseModel):
    """Registration response with user and tokens."""

    user: UserResponse
    message: str = "User registered successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "role": "user",
                    "full_name": "John Doe",
                    "is_active": True,
                    "created_at": "2026-07-16T10:00:00Z",
                },
                "message": "User registered successfully",
            }
        }


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str
    detail: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful",
                "detail": "Additional information if needed",
            }
        }


# ============================================================================
# Error Response Schemas
# ============================================================================


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: str
    status_code: int

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Unauthorized",
                "detail": "Invalid credentials",
                "status_code": 401,
            }
        }

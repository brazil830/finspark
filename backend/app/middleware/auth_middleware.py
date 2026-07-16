"""Authentication middleware."""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware to extract and validate user authentication."""

    # Endpoints that don't require authentication
    EXCLUDED_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Extract and validate authentication."""
        # Skip auth for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # Extract user from Authorization header or cookies
        auth_header = request.headers.get("Authorization", "")
        cookies = request.cookies

        # For now, we add basic user context to request state
        # In production, this would validate tokens and extract actual user info
        request.state.user = None
        request.state.user_id = None
        request.state.user_role = None

        # Try to extract from Authorization header (Bearer token)
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            request.state.auth_token = token
            # In production: validate token here

        # Try to extract from cookies
        if "session_id" in cookies:
            request.state.session_id = cookies["session_id"]

        # Call next middleware/route
        response = await call_next(request)

        return response

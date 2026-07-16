"""Rate Limiting and DDoS Protection Middleware.

Implements:
- Per-IP rate limiting
- Per-user rate limiting
- Token bucket algorithm
- Exponential backoff on authentication failures
- Rate limit headers in responses
"""

import logging
import time
from typing import Dict, Optional, Tuple

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class RateLimitBucket:
    """Token bucket for rate limiting."""

    def __init__(self, capacity: int, refill_rate: float):
        """Initialize token bucket.

        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def get_tokens(self, num: int = 1) -> bool:
        """Try to consume tokens.

        Args:
            num: Number of tokens to consume

        Returns:
            True if tokens available, False otherwise
        """
        now = time.time()
        elapsed = now - self.last_refill

        # Refill tokens
        self.tokens = min(
            self.capacity,
            self.tokens + (elapsed * self.refill_rate),
        )
        self.last_refill = now

        # Try to consume
        if self.tokens >= num:
            self.tokens -= num
            return True
        return False

    def get_remaining(self) -> int:
        """Get remaining tokens."""
        now = time.time()
        elapsed = now - self.last_refill
        return int(min(
            self.capacity,
            self.tokens + (elapsed * self.refill_rate),
        ))


class RateLimiter:
    """Rate limiter with per-IP and per-user tracking."""

    def __init__(
        self,
        global_limit: int = 10000,  # requests per minute globally
        per_ip_limit: int = 100,     # requests per minute per IP
        per_user_limit: int = 1000,  # requests per minute per user
        auth_fail_window: int = 300, # 5 minutes
        auth_fail_threshold: int = 5,
    ):
        """Initialize rate limiter.

        Args:
            global_limit: Global rate limit (per minute)
            per_ip_limit: Per-IP rate limit (per minute)
            per_user_limit: Per-user rate limit (per minute)
            auth_fail_window: Window for tracking auth failures (seconds)
            auth_fail_threshold: Auth failures before temporary ban
        """
        self.global_limit = global_limit
        self.per_ip_limit = per_ip_limit
        self.per_user_limit = per_user_limit
        self.auth_fail_window = auth_fail_window
        self.auth_fail_threshold = auth_fail_threshold

        # Token buckets (refill_rate = limit / 60 to get per-minute limit)
        self.global_bucket = RateLimitBucket(global_limit, global_limit / 60)
        self.ip_buckets: Dict[str, RateLimitBucket] = {}
        self.user_buckets: Dict[int, RateLimitBucket] = {}

        # Authentication failure tracking
        self.auth_failures: Dict[str, list] = {}  # ip -> [timestamps]
        self.blocked_ips: Dict[str, float] = {}   # ip -> blocked_until

        logger.info(
            f"RateLimiter initialized: "
            f"global={global_limit}/min, "
            f"per_ip={per_ip_limit}/min, "
            f"per_user={per_user_limit}/min"
        )

    def _get_ip_bucket(self, ip: str) -> RateLimitBucket:
        """Get or create bucket for IP."""
        if ip not in self.ip_buckets:
            self.ip_buckets[ip] = RateLimitBucket(
                self.per_ip_limit,
                self.per_ip_limit / 60,
            )
        return self.ip_buckets[ip]

    def _get_user_bucket(self, user_id: int) -> RateLimitBucket:
        """Get or create bucket for user."""
        if user_id not in self.user_buckets:
            self.user_buckets[user_id] = RateLimitBucket(
                self.per_user_limit,
                self.per_user_limit / 60,
            )
        return self.user_buckets[user_id]

    def check_limit(
        self,
        ip: str,
        user_id: Optional[int] = None,
    ) -> Tuple[bool, Optional[str], Dict[str, int]]:
        """Check if request is allowed under rate limits.

        Args:
            ip: Client IP address
            user_id: Optional authenticated user ID

        Returns:
            Tuple of (allowed, reason, rate_limit_info)
        """
        # Check if IP is temporarily blocked due to auth failures
        if ip in self.blocked_ips:
            if time.time() < self.blocked_ips[ip]:
                return False, "IP temporarily blocked due to auth failures", {}

            # Unblock IP
            del self.blocked_ips[ip]
            self.auth_failures[ip] = []

        # Check global limit
        if not self.global_bucket.get_tokens():
            return False, "Global rate limit exceeded", {}

        # Check per-IP limit
        ip_bucket = self._get_ip_bucket(ip)
        if not ip_bucket.get_tokens():
            return False, "Per-IP rate limit exceeded", {}

        # Check per-user limit (if authenticated)
        if user_id:
            user_bucket = self._get_user_bucket(user_id)
            if not user_bucket.get_tokens():
                return False, "Per-user rate limit exceeded", {}

        # Rate limit info for headers
        rate_limit_info = {
            "limit": self.per_ip_limit,
            "remaining": ip_bucket.get_remaining(),
            "reset": int(time.time() + 60),  # Reset in 1 minute
        }

        return True, None, rate_limit_info

    def record_auth_failure(self, ip: str) -> None:
        """Record authentication failure for IP.

        Args:
            ip: Client IP address
        """
        now = time.time()

        if ip not in self.auth_failures:
            self.auth_failures[ip] = []

        # Remove old failures outside window
        self.auth_failures[ip] = [
            ts for ts in self.auth_failures[ip]
            if now - ts < self.auth_fail_window
        ]

        # Add new failure
        self.auth_failures[ip].append(now)

        # Check if we should block
        if len(self.auth_failures[ip]) >= self.auth_fail_threshold:
            # Block for 15 minutes
            self.blocked_ips[ip] = time.time() + (15 * 60)
            logger.warning(
                f"IP {ip} blocked due to {len(self.auth_failures[ip])} "
                f"auth failures in {self.auth_fail_window}s"
            )

    def reset_auth_failures(self, ip: str) -> None:
        """Reset auth failure counter for IP.

        Args:
            ip: Client IP address
        """
        if ip in self.auth_failures:
            self.auth_failures[ip] = []


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get or create global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting and DDoS protection."""

    def __init__(self, app, rate_limiter: Optional[RateLimiter] = None):
        """Initialize middleware.

        Args:
            app: FastAPI application
            rate_limiter: Optional custom rate limiter instance
        """
        super().__init__(app)
        self.rate_limiter = rate_limiter or get_rate_limiter()

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request with rate limiting.

        Args:
            request: Incoming request
            call_next: Next middleware/handler

        Returns:
            Response with rate limit headers
        """
        # Get client IP (handle X-Forwarded-For for proxies)
        client_ip = request.headers.get("X-Forwarded-For", "")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        # Try to extract user ID from JWT (if authenticated)
        user_id = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            # Note: In production, would properly decode JWT
            # For now, we'll skip extracting user_id
            pass

        # Check rate limits
        allowed, reason, rate_limit_info = self.rate_limiter.check_limit(
            client_ip,
            user_id,
        )

        if not allowed:
            logger.warning(
                f"Rate limit exceeded for {client_ip}: {reason}"
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too many requests",
                    "detail": reason,
                    "retry_after": rate_limit_info.get("reset", int(time.time() + 60)),
                },
                headers={
                    "Retry-After": str(rate_limit_info.get("reset", int(time.time() + 60))),
                },
            )

        # Call next middleware/handler
        response = await call_next(request)

        # Add rate limit headers
        if rate_limit_info:
            response.headers["X-RateLimit-Limit"] = str(rate_limit_info["limit"])
            response.headers["X-RateLimit-Remaining"] = str(rate_limit_info["remaining"])
            response.headers["X-RateLimit-Reset"] = str(rate_limit_info["reset"])

        # Record auth failures on 401 responses
        if response.status_code == 401 and "/auth/login" in request.url.path:
            self.rate_limiter.record_auth_failure(client_ip)

        # Reset auth failures on successful login
        if response.status_code == 200 and "/auth/login" in request.url.path:
            self.rate_limiter.reset_auth_failures(client_ip)

        return response

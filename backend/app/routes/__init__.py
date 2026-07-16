"""API route handlers."""

from app.routes.agent import router_agent
from app.routes.analytics import router_analytics
from app.routes.auth import router
from app.routes.crypto import router_crypto
from app.routes.dashboard import router_dashboard
from app.routes.database import router_database
from app.routes.deception import router_deception

router_auth = router

__all__ = [
    "router_agent",
    "router_analytics",
    "router_auth",
    "router_crypto",
    "router_dashboard",
    "router_database",
    "router_deception",
]

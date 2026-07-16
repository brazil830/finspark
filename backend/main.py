"""RAG-Sec Standalone Backend - Main FastAPI Application Entry Point."""

import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.middleware import (
    AuthenticationMiddleware,
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from app.routes import (
    router_agent,
    router_analytics,
    router_crypto,
    router_dashboard,
    router_database,
    router_deception,
    router_auth,
)
from app.services import get_db_manager, get_honey_detector, get_hsm_manager

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager - handles startup and shutdown events.

    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown")
    patterns with a single context manager.
    """
    # Startup event
    logger.info("=" * 60)
    logger.info("RAG-Sec Standalone Backend Starting Up")
    logger.info("=" * 60)

    try:
        # Initialize database connections
        db_manager = get_db_manager()
        logger.info("Initializing database connections...")
        await db_manager.initialize(
            database_url=settings.DATABASE_URL,
            sqlite_path=settings.SQLITE_DB_PATH,
        )
        logger.info("[OK] Database connections initialized")

        # Initialize HSM key manager
        hsm_manager = get_hsm_manager()
        hsm_manager.initialize()
        logger.info(f"[OK] HSM initialized with key: {hsm_manager.get_current_key_id()}")

        # Initialize honey table detector
        honey_detector = get_honey_detector()
        stats = honey_detector.get_detection_stats()
        logger.info(
            f"[OK] Honey table detector initialized with "
            f"{stats['honey_table_count']} tables"
        )

        logger.info(f"Application ready at http://{settings.HOST}:{settings.PORT}")
        logger.info(f"API documentation at http://{settings.HOST}:{settings.PORT}/docs")
        logger.info("=" * 60)

        yield  # Application runs here

    except Exception as e:
        logger.error(f"Startup failed: {e}", exc_info=True)
        raise

    finally:
        # Shutdown event
        logger.info("=" * 60)
        logger.info("RAG-Sec Standalone Backend Shutting Down")
        logger.info("=" * 60)

        try:
            # Close database connections
            db_manager = get_db_manager()
            await db_manager.close()
            logger.info("[OK] Database connections closed")

        except Exception as e:
            logger.error(f"Shutdown error: {e}", exc_info=True)

        logger.info("Application shutdown complete")
        logger.info("=" * 60)


# Create FastAPI application with custom lifespan
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan,
)

logger.info(f"FastAPI app created: {settings.APP_TITLE} v{settings.APP_VERSION}")

# ============================================================================
# MIDDLEWARE CONFIGURATION (order matters - added in reverse execution order)
# ============================================================================

# Add CORS middleware (outermost/last to execute)
logger.info(f"Configuring CORS with origins: {settings.CORS_ORIGINS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Add rate limiting middleware
logger.info("Configuring rate limiting middleware")
app.add_middleware(RateLimitMiddleware)

# Add security headers middleware
logger.info("Configuring security headers middleware")
app.add_middleware(SecurityHeadersMiddleware)

# Add authentication middleware
logger.info("Configuring authentication middleware")
app.add_middleware(AuthenticationMiddleware)

# Add request logging middleware
logger.info("Configuring request logging middleware")
app.add_middleware(RequestLoggingMiddleware)

logger.info("[OK] All middleware configured")

# ============================================================================
# GLOBAL EXCEPTION HANDLERS
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"[{request_id}] Unhandled exception: {exc}",
        exc_info=True,
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handler for validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        f"[{request_id}] Validation error: {exc}",
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "request_id": request_id,
        },
    )


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint.

    Returns:
        JSON with health status and version information
    """
    db_manager = get_db_manager()
    hsm_manager = get_hsm_manager()

    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "service": settings.APP_TITLE,
        "database": "connected" if db_manager.pg_engine else "disconnected",
        "hsm_key_id": hsm_manager.get_current_key_id(),
        "hsm_key_age_minutes": round(hsm_manager.get_key_age_minutes(), 2),
    }


# ============================================================================
# ROUTE REGISTRATION
# ============================================================================

logger.info(f"Registering API routes with prefix: {settings.API_PREFIX}")

# Register all route modules with API prefix
app.include_router(router_auth, prefix=settings.API_PREFIX)
app.include_router(router_dashboard, prefix=settings.API_PREFIX)
app.include_router(router_agent, prefix=settings.API_PREFIX)
app.include_router(router_crypto, prefix=settings.API_PREFIX)
app.include_router(router_deception, prefix=settings.API_PREFIX)
app.include_router(router_analytics, prefix=settings.API_PREFIX)
app.include_router(router_database, prefix=settings.API_PREFIX)

logger.info(
    "[OK] Registered routes: auth, dashboard, agent, crypto, deception, analytics, database"
)

# ============================================================================
# ROOT ENDPOINT
# ============================================================================


@app.get("/", tags=["info"])
async def root():
    """Root endpoint providing API information.

    Returns:
        JSON with API information and available endpoints
    """
    return {
        "name": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "health": "/health",
        "api_prefix": settings.API_PREFIX,
        "endpoints": {
            "dashboard": f"{settings.API_PREFIX}/dashboard",
            "agent": f"{settings.API_PREFIX}/agent",
            "crypto": f"{settings.API_PREFIX}/crypto",
            "deception": f"{settings.API_PREFIX}/deception",
            "analytics": f"{settings.API_PREFIX}/analytics",
            "database": f"{settings.API_PREFIX}/database",
        },
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main entry point for running the application with uvicorn."""
    logger.info(
        f"Starting uvicorn server on {settings.HOST}:{settings.PORT} "
        f"(debug={settings.DEBUG})"
    )

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application failed: {e}", exc_info=True)
        sys.exit(1)

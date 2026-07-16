#!/usr/bin/env python
"""Verification script to check if main.py setup is complete and working."""

import sys
from pathlib import Path

# Add backend to path
backend_root = Path(__file__).parent
sys.path.insert(0, str(backend_root))


def check_imports():
    """Check if all required imports work."""
    print("Checking imports...")
    errors = []

    try:
        from app.config.settings import settings
        print("  [OK] app.config.settings")
    except Exception as e:
        errors.append(f"  [FAIL] app.config.settings: {e}")

    try:
        from app.middleware import (
            AuthenticationMiddleware,
            RequestLoggingMiddleware,
            SecurityHeadersMiddleware,
        )
        print("  [OK] app.middleware")
    except Exception as e:
        errors.append(f"  [FAIL] app.middleware: {e}")

    try:
        from app.routes import (
            router_agent,
            router_analytics,
            router_crypto,
            router_dashboard,
            router_database,
            router_deception,
        )
        print("  [OK] app.routes")
    except Exception as e:
        errors.append(f"  [FAIL] app.routes: {e}")

    try:
        from app.services import (
            get_db_manager,
            get_honey_detector,
            get_hsm_manager,
        )
        print("  [OK] app.services")
    except Exception as e:
        errors.append(f"  [FAIL] app.services: {e}")

    try:
        import main  # noqa: F401
        print("  [OK] main.py")
    except Exception as e:
        errors.append(f"  [FAIL] main.py: {e}")

    return errors


def check_files():
    """Check if required files exist."""
    print("\nChecking required files...")
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "app/__init__.py",
        "app/config/__init__.py",
        "app/config/settings.py",
        "app/middleware/__init__.py",
        "app/middleware/logging_middleware.py",
        "app/middleware/security_headers_middleware.py",
        "app/middleware/auth_middleware.py",
        "app/routes/__init__.py",
        "app/routes/dashboard.py",
        "app/routes/agent.py",
        "app/routes/crypto.py",
        "app/routes/deception.py",
        "app/routes/analytics.py",
        "app/routes/database.py",
        "app/services/__init__.py",
        "app/services/database.py",
        "app/services/hsm.py",
        "app/services/honey_detector.py",
    ]

    missing = []
    for file_path in required_files:
        full_path = backend_root / file_path
        if full_path.exists():
            print(f"  [OK] {file_path}")
        else:
            missing.append(f"  [FAIL] {file_path} (missing)")

    return missing


def check_configuration():
    """Check if configuration loads correctly."""
    print("\nChecking configuration...")
    errors = []

    try:
        from app.config.settings import settings

        required_settings = [
            "APP_TITLE",
            "APP_VERSION",
            "HOST",
            "PORT",
            "API_PREFIX",
            "DATABASE_URL",
            "SQLITE_DB_PATH",
        ]

        for setting in required_settings:
            value = getattr(settings, setting, None)
            if value is not None:
                print(f"  [OK] {setting}: {value}")
            else:
                errors.append(f"  [FAIL] {setting}: not set")

    except Exception as e:
        errors.append(f"Configuration loading failed: {e}")

    return errors


def check_services():
    """Check if services initialize correctly."""
    print("\nChecking services...")
    errors = []

    try:
        from app.services import get_db_manager, get_hsm_manager, get_honey_detector

        # Check HSM manager
        hsm = get_hsm_manager()
        hsm.initialize()
        print(f"  [OK] HSM Manager initialized with key: {hsm.get_current_key_id()}")

        # Check Honey Detector
        honey = get_honey_detector()
        stats = honey.get_detection_stats()
        print(f"  [OK] Honey Detector initialized with {stats['honey_table_count']} tables")

        # Check DB Manager exists
        db = get_db_manager()
        print("  [OK] Database Manager initialized")

    except Exception as e:
        errors.append(f"Service initialization failed: {e}")

    return errors


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("RAG-Sec Backend - Setup Verification")
    print("=" * 60)

    all_errors = []

    # Check files
    file_errors = check_files()
    all_errors.extend(file_errors)

    # Check imports
    import_errors = check_imports()
    all_errors.extend(import_errors)

    # Check configuration
    config_errors = check_configuration()
    all_errors.extend(config_errors)

    # Check services
    service_errors = check_services()
    all_errors.extend(service_errors)

    # Summary
    print("\n" + "=" * 60)
    if not all_errors:
        print("[OK] ALL CHECKS PASSED")
        print("=" * 60)
        print("\nYour RAG-Sec backend is ready!")
        print("Start the application with: python main.py")
        print("Access the API at: http://localhost:8000")
        print("View docs at: http://localhost:8000/docs")
        return 0
    else:
        print(f"[FAIL] {len(all_errors)} ISSUE(S) FOUND:")
        print("=" * 60)
        for error in all_errors:
            print(error)
        print("\n" + "=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

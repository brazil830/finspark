"""Debug session d64954: diagnose ModuleNotFoundError for sqlalchemy."""
import json
import sys
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "debug-d64954.log"


def _log(hypothesis_id: str, location: str, message: str, data: dict, run_id: str = "pre-fix") -> None:
    # #region agent log
    payload = {
        "sessionId": "d64954",
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": __import__("time").time() * 1000,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    # #endregion


def main() -> int:
    venv_dir = Path(__file__).resolve().parent / "venv"
    site_packages = venv_dir / "Lib" / "site-packages"

    # Hypothesis A: requirements install failed before sqlalchemy was installed
    dist_names = sorted(p.name for p in site_packages.glob("*") if p.is_dir() or p.suffix == ".dist-info")
    installed = [n for n in dist_names if "sqlalchemy" in n.lower() or "pyjwt" in n.lower() or "fastapi" in n.lower()]
    _log(
        "A",
        "debug_env_check.py:main",
        "venv site-packages snapshot",
        {
            "sqlalchemy_or_fastapi_installed": installed,
            "total_entries": len(dist_names),
            "has_aiosqlite": any("aiosqlite" in n.lower() for n in dist_names),
        },
    )

    # Hypothesis B/D: wrong interpreter despite venv activation
    _log(
        "B",
        "debug_env_check.py:main",
        "python interpreter info",
        {
            "executable": sys.executable,
            "version": sys.version,
            "in_venv": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
            "expected_venv_python": str(venv_dir / "Scripts" / "python.exe"),
            "using_venv_python": str(Path(sys.executable).resolve()) == str((venv_dir / "Scripts" / "python.exe").resolve()),
        },
    )

    # Hypothesis C: sqlalchemy import path issue
    try:
        import sqlalchemy  # noqa: F401
        import_ok = True
        import_error = None
        sqlalchemy_file = getattr(sqlalchemy, "__file__", None)
    except Exception as exc:  # noqa: BLE001
        import_ok = False
        import_error = repr(exc)
        sqlalchemy_file = None

    _log(
        "C",
        "debug_env_check.py:main",
        "sqlalchemy import attempt",
        {"import_ok": import_ok, "import_error": import_error, "sqlalchemy_file": sqlalchemy_file},
    )

    # Hypothesis E: pip freeze shows partial install state
    import subprocess

    pip_freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=False,
    )
    freeze_lines = [line for line in pip_freeze.stdout.splitlines() if line]
    _log(
        "E",
        "debug_env_check.py:main",
        "pip freeze in active interpreter",
        {
            "returncode": pip_freeze.returncode,
            "package_count": len(freeze_lines),
            "packages": freeze_lines[:20],
            "stderr_tail": pip_freeze.stderr[-300:] if pip_freeze.stderr else "",
        },
    )

    return 0 if import_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

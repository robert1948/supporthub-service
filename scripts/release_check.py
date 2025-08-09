import os
import sys
import subprocess
from fastapi.testclient import TestClient


def _normalize_db_url():
    url = os.getenv("DATABASE_URL")
    if url and url.startswith("postgres://"):
        os.environ["DATABASE_URL"] = "postgresql://" + url[len("postgres://"):]


def _run(cmd: list[str]) -> int:
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)


def main() -> int:
    _normalize_db_url()

    # Run migrations if Alembic is present
    try:
        rc = _run([sys.executable, "-m", "alembic", "upgrade", "head"])
        if rc != 0:
            print("Alembic upgrade failed", file=sys.stderr)
            return rc
    except Exception as e:
        print(f"Alembic not available or failed to run: {e}", file=sys.stderr)
        return 1

    # Import app and run health probe
    try:
        from app.main import app
        client = TestClient(app)
        resp = client.get("/health")
        ok = resp.status_code == 200
        print("Health:", resp.json())
        return 0 if ok else 1
    except Exception as e:
        print(f"Release check exception: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

import os
import sys
from fastapi.testclient import TestClient


def _normalize_db_url():
    url = os.getenv("DATABASE_URL")
    if url and url.startswith("postgres://"):
        os.environ["DATABASE_URL"] = "postgresql://" + url[len("postgres://"):]


def main() -> int:
    try:
        _normalize_db_url()
        from app.main import app  # import after env normalization
    except Exception as e:
        print(f"Release check import failed: {e}", file=sys.stderr)
        return 1

    try:
        client = TestClient(app)
        resp = client.get("/")
        if resp.status_code != 200:
            print(f"Release check failed: {resp.status_code} {resp.text}", file=sys.stderr)
            return 1
        print("Release check OK:", resp.json())
        return 0
    except Exception as e:
        print(f"Release check exception: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

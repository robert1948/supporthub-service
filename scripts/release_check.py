import sys
from fastapi.testclient import TestClient

try:
    from app.main import app
except Exception as e:
    print(f"Release check import failed: {e}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
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

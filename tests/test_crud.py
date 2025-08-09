import os
import time
import pytest
import httpx

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")

@pytest.fixture(scope="session", autouse=True)
def wait_for_api():
    # Wait briefly for API to be up when running in compose
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            r = httpx.get(f"{API_URL}/health", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    pytest.fail("API did not become ready in time")


def _headers():
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["X-API-Key"] = API_KEY
    return h


def test_ticket_crud():
    # Create
    resp = httpx.post(
        f"{API_URL}/v1/tickets/",
        json={"title": "Test Ticket", "description": "Hello"},
        headers=_headers(),
    )
    assert resp.status_code == 201, resp.text
    ticket = resp.json()
    tid = ticket["id"]

    # Read
    resp = httpx.get(f"{API_URL}/v1/tickets/{tid}", headers=_headers())
    assert resp.status_code == 200
    assert resp.json()["title"] == "Test Ticket"

    # List with filter
    resp = httpx.get(f"{API_URL}/v1/tickets/?q=Test", headers=_headers())
    assert resp.status_code == 200
    assert any(t["id"] == tid for t in resp.json())

    # Update (status)
    resp = httpx.patch(
        f"{API_URL}/v1/tickets/{tid}", json={"status": "closed"}, headers=_headers()
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"


def test_message_crud():
    # Create a ticket first
    resp = httpx.post(
        f"{API_URL}/v1/tickets/",
        json={"title": "Ticket for message", "description": None},
        headers=_headers(),
    )
    assert resp.status_code == 201
    tid = resp.json()["id"]

    # Create message
    resp = httpx.post(
        f"{API_URL}/v1/messages/",
        json={"ticket_id": tid, "content": "First msg"},
        headers=_headers(),
    )
    assert resp.status_code == 201, resp.text
    mid = resp.json()["id"]

    # Get message
    resp = httpx.get(f"{API_URL}/v1/messages/{mid}", headers=_headers())
    assert resp.status_code == 200

    # List messages filtered by ticket
    resp = httpx.get(f"{API_URL}/v1/messages/?ticket_id={tid}", headers=_headers())
    assert resp.status_code == 200
    data = resp.json()
    assert any(m["id"] == mid for m in data)

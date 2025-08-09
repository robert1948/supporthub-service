from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_tickets():
    return [{"id": 1, "title": "Example Ticket"}]

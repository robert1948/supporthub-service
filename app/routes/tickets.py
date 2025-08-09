from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

# In-memory store for demo purposes
_TICKETS: dict[int, dict] = {
    1: {"id": 1, "title": "Example Ticket", "status": "open"}
}
_next_id = 2

class TicketIn(BaseModel):
    title: str = Field(..., min_length=3)
    description: str | None = None

class TicketOut(TicketIn):
    id: int
    status: str = "open"

@router.get("/", response_model=List[TicketOut])
def list_tickets():
    return list(_TICKETS.values())

@router.post("/", response_model=TicketOut, status_code=201)
def create_ticket(data: TicketIn):
    global _next_id
    t = {"id": _next_id, "title": data.title, "description": data.description, "status": "open"}
    _TICKETS[_next_id] = t
    _next_id += 1
    return t

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int):
    t = _TICKETS.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t

@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket_status(ticket_id: int, status: str = "open"):
    t = _TICKETS.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t["status"] = status
    return t

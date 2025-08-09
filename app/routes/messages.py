from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

_MESSAGES: dict[int, dict] = {1: {"id": 1, "ticket_id": 1, "content": "Example Message"}}
_next_msg_id = 2

class MessageIn(BaseModel):
    ticket_id: int
    content: str = Field(..., min_length=1)

class MessageOut(MessageIn):
    id: int

@router.get("/", response_model=List[MessageOut])
def list_messages():
    return list(_MESSAGES.values())

@router.post("/", response_model=MessageOut, status_code=201)
def create_message(data: MessageIn):
    global _next_msg_id
    m = {"id": _next_msg_id, "ticket_id": data.ticket_id, "content": data.content}
    _MESSAGES[_next_msg_id] = m
    _next_msg_id += 1
    return m

@router.get("/{message_id}", response_model=MessageOut)
def get_message(message_id: int):
    m = _MESSAGES.get(message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    return m

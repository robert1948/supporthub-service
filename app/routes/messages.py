from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Message, Ticket
from app.schemas.messages import MessageCreate, MessageRead

router = APIRouter()

@router.get("/", response_model=List[MessageRead])
def list_messages(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    ticket_id: int | None = Query(None),
):
    query = db.query(Message)
    if ticket_id is not None:
        query = query.filter(Message.ticket_id == ticket_id)
    items = query.order_by(Message.created_at.desc()).offset(offset).limit(limit).all()
    return items

@router.post("/", response_model=MessageRead, status_code=201)
def create_message(data: MessageCreate, db: Session = Depends(get_db)):
    # Ensure ticket exists
    t = db.get(Ticket, data.ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    m = Message(ticket_id=data.ticket_id, content=data.content)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/{message_id}", response_model=MessageRead)
def get_message(message_id: int, db: Session = Depends(get_db)):
    m = db.get(Message, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    return m

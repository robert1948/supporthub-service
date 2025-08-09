from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Ticket
from app.schemas.tickets import TicketCreate, TicketUpdate, TicketRead

router = APIRouter()

@router.get("/", response_model=List[TicketRead])
def list_tickets(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="Search in title/description"),
):
    query = db.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    if q:
        like = f"%{q}%"
        query = query.filter((Ticket.title.ilike(like)) | (Ticket.description.ilike(like)))
    items = query.order_by(Ticket.created_at.desc()).offset(offset).limit(limit).all()
    return items

@router.post("/", response_model=TicketRead, status_code=201)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db)):
    t = Ticket(title=data.title, description=data.description)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    t = db.get(Ticket, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t

@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: int, data: TicketUpdate, db: Session = Depends(get_db)):
    t = db.get(Ticket, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # Apply partial updates
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(t, field, value)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

class TicketUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(default=None, min_length=2, max_length=32)

class TicketRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

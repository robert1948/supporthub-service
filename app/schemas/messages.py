from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class MessageCreate(BaseModel):
    ticket_id: int
    content: str = Field(..., min_length=1)

class MessageRead(BaseModel):
    id: int
    ticket_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

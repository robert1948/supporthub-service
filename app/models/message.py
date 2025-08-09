from __future__ import annotations
from sqlalchemy import Integer, String, Text, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)

    ticket = relationship("Ticket", backref="messages")

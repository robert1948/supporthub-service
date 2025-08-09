from __future__ import annotations
from typing import Generator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    pass

_engine = None
SessionLocal: Optional[sessionmaker] = None

if settings.DATABASE_URL:
    _engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_engine():
    return _engine


def get_sessionmaker():
    return SessionLocal


def db_health() -> str:
    if not _engine:
        return "disabled"
    try:
        with _engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "up"
    except Exception:
        return "down"


def get_db() -> Generator:
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

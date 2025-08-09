from __future__ import annotations
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

if not settings.DATABASE_URL:
    # Default to in-memory SQLite for dev if DATABASE_URL not provided
    SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
    connect_args = {"check_same_thread": False}
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    connect_args = {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

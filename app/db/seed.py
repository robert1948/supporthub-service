from __future__ import annotations
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Connection

# Example seed data helper for development/testing

def seed_basic_data(conn: Connection):
    metadata = MetaData(bind=conn)
    # Tables reflect only if needed; keeping placeholder for future seeds
    # metadata.reflect(only=["tickets", "messages"])  # noqa: ERA001
    pass

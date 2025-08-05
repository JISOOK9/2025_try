import os
from contextlib import contextmanager
from typing import List, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

_engine: Optional[Engine] = None


def get_engine(url: Optional[str] = None) -> Engine:
    """Return a singleton SQLAlchemy engine.

    Parameters
    ----------
    url: Optional[str]
        Override the database URL. If not provided, ``DATABASE_URL``
        environment variable is used or falls back to in-memory SQLite.
    """
    global _engine
    if url:
        _engine = create_engine(url)
    elif _engine is None:
        db_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
        _engine = create_engine(db_url)
    return _engine


@contextmanager
def get_connection(url: Optional[str] = None):
    """Yield a database connection."""
    engine = get_engine(url)
    with engine.connect() as conn:
        yield conn


def fetch_user_subscriptions(user_id: int, conn=None) -> List[str]:
    """Return a list of subscription names for ``user_id``."""
    query = text("SELECT name FROM subscriptions WHERE user_id = :uid")
    if conn is None:
        with get_connection() as conn:
            result = conn.execute(query, {"uid": user_id})
            return [row[0] for row in result]
    result = conn.execute(query, {"uid": user_id})
    return [row[0] for row in result]

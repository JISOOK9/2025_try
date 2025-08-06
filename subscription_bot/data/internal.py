"""Mock internal database access for user information."""
from __future__ import annotations

from typing import Dict, List

# In a real application this would query a database. Here we keep a simple
# in-memory structure to simulate stored user data.
_DATABASE: Dict[int, Dict[str, object]] = {
    1: {"user_id": 1, "name": "Alice", "subscriptions": ["넷플릭스"]},
    2: {"user_id": 2, "name": "Bob", "subscriptions": []},
}


def get_user_info(user_id: int) -> Dict[str, object]:
    """Return information for ``user_id`` from the internal database."""
    return _DATABASE.get(user_id, {"user_id": user_id, "subscriptions": []})

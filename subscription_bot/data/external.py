"""Mock external crawler providing additional user context."""
from __future__ import annotations

from typing import Dict

# Real implementation would crawl the web for latest information about
# the user's subscriptions or interests. For tests we simply return
# static data keyed by ``user_id``.
_CRAWLED: Dict[int, Dict[str, object]] = {
    1: {"reviews": [{"title": "Great service", "source": "web"}]},
    2: {"reviews": []},
}


def crawl_user_data(user_id: int) -> Dict[str, object]:
    """Return externally gathered data for ``user_id``."""
    return _CRAWLED.get(user_id, {"reviews": []})

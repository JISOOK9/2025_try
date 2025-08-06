"""Service layer combining internal and external data sources."""
from __future__ import annotations

from typing import Any, Dict

from . import external, internal


def build_user_context(user_id: int) -> Dict[str, Any]:
    """Build a unified context dictionary for ``user_id``.

    This function orchestrates calls to the internal database access layer
    and the external crawler. Data from both sources is merged into a single
    dictionary that can be passed to higher level chatbot components.

    Parameters
    ----------
    user_id:
        Identifier for the user whose context should be built.

    Returns
    -------
    dict
        A dictionary containing merged user information.
    """
    context: Dict[str, Any] = {}

    # Fetch internal information first; this forms the base context.
    internal_data = internal.get_user_info(user_id)
    context.update(internal_data)

    # Retrieve external/crawled data and merge.
    external_data = external.crawl_user_data(user_id)
    for key, value in external_data.items():
        if key in context and isinstance(context[key], list) and isinstance(value, list):
            context[key] = context[key] + value
        elif key in context and isinstance(context[key], dict) and isinstance(value, dict):
            context[key].update(value)
        else:
            context[key] = value

    return context

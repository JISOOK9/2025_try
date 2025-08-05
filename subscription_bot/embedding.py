"""Utilities for masking personal information and embedding user context."""
from __future__ import annotations

from typing import Any, Dict, List

# Fields considered personally identifiable information (PII)
PII_FIELDS = {"user_id", "email", "phone", "address", "name", "card_number"}


def mask_personal_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``data`` with personal fields removed.

    Parameters
    ----------
    data: dict
        Original context dictionary possibly containing PII.

    Returns
    -------
    dict
        New dictionary without keys that correspond to PII.
    """
    return {k: v for k, v in data.items() if k not in PII_FIELDS}


def embed_context(data: Dict[str, Any]) -> List[float]:
    """Embed subscription context into a numeric vector.

    The function first removes PII fields via :func:`mask_personal_info` and
    then converts remaining information such as subscription list and payment
    amount into a deterministic numeric feature vector. Each subscription is
    represented as a binary feature and the payment amount is included as a
    numeric value.

    Parameters
    ----------
    data: dict
        Context dictionary which may contain fields like ``subscriptions``
        (list of service names) and ``payment_amount`` (numeric).

    Returns
    -------
    list[float]
        Sorted list of feature values representing the context.
    """
    sanitized = mask_personal_info(data)

    subscriptions = sanitized.get("subscriptions", []) or []
    payment_amount = float(sanitized.get("payment_amount", 0))

    features: Dict[str, float] = {
        f"subscription={sub}": 1.0 for sub in subscriptions
    }
    features["payment_amount"] = payment_amount

    # Sort feature names to ensure deterministic ordering
    return [features[key] for key in sorted(features)]

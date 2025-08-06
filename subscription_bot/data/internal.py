"""Internal data access layer for subscription information.

Provides functions to fetch subscription status, payment history, and
product metadata using a pluggable storage backend.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


class StorageBackend(Protocol):
    """Protocol for storage backend implementations."""

    def get_user_subscription_state(self, user_id: str) -> Dict[str, Any]:
        """Return subscription state for a user."""

    def get_payment_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Return payment history for a user."""

    def get_product_metadata(self, product_id: str) -> Dict[str, Any]:
        """Return metadata for a product."""


@dataclass
class InMemoryStorage:
    """Simple in-memory storage backend.

    Useful for testing or prototyping. Real implementations can swap in a
    database-backed storage by implementing :class:`StorageBackend`.
    """

    subscriptions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    payments: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    products: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def get_user_subscription_state(self, user_id: str) -> Dict[str, Any]:
        return self.subscriptions.get(user_id, {})

    def get_payment_history(self, user_id: str) -> List[Dict[str, Any]]:
        return self.payments.get(user_id, [])

    def get_product_metadata(self, product_id: str) -> Dict[str, Any]:
        return self.products.get(product_id, {})


_storage_backend: StorageBackend = InMemoryStorage()


def set_storage_backend(backend: StorageBackend) -> None:
    """Configure the global storage backend."""

    global _storage_backend
    _storage_backend = backend


def get_user_subscription_state(user_id: str) -> Dict[str, Any]:
    """Fetch subscription state for ``user_id`` from the storage backend."""

    return _storage_backend.get_user_subscription_state(user_id)


def get_payment_history(user_id: str) -> List[Dict[str, Any]]:
    """Fetch payment history for ``user_id`` from the storage backend."""

    return _storage_backend.get_payment_history(user_id)


def get_product_metadata(product_id: str) -> Dict[str, Any]:
    """Fetch metadata for ``product_id`` from the storage backend."""

    return _storage_backend.get_product_metadata(product_id)

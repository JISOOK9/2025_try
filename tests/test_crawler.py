"""Tests for the crawler module."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

import pytest

from subscription_bot import crawler


class DummyResponse(SimpleNamespace):
    """Simple mock object for ``requests`` responses."""

    def raise_for_status(self) -> None:  # pragma: no cover - trivial
        return None


def test_crawl_review(monkeypatch: pytest.MonkeyPatch) -> None:
    html = """
    <html><head><title>Review Title</title></head>
    <body><p>Review text.</p></body></html>
    """

    dummy_resp = DummyResponse(text=html)
    monkeypatch.setattr(crawler.requests, "get", lambda url, timeout=10: dummy_resp)

    class DummyDatetime(datetime):
        @classmethod
        def utcnow(cls):  # type: ignore[override]
            return cls(2023, 1, 1)

    monkeypatch.setattr(crawler, "datetime", DummyDatetime)

    result = crawler.crawl_review("http://example.com")
    assert result == {
        "title": "Review Title",
        "content": "Review text.",
        "source": "unknown",
        "published_at": "2023-01-01",
        "price": None,
    }


def test_crawl_news(monkeypatch: pytest.MonkeyPatch) -> None:
    html = """
    <html><head><title>News Title</title></head>
    <body>
        <time datetime="2024-02-10T08:00:00Z">Feb 10</time>
        <p>News content here.</p>
    </body></html>
    """

    dummy_resp = DummyResponse(text=html)
    monkeypatch.setattr(crawler.requests, "get", lambda url, timeout=10: dummy_resp)

    result = crawler.crawl_news("http://example.com/news", source="NewsSite")
    assert result == {
        "title": "News Title",
        "content": "News content here.",
        "source": "NewsSite",
        "published_at": "2024-02-10",
        "price": None,
    }


def test_crawl_price(monkeypatch: pytest.MonkeyPatch) -> None:
    html = """
    <html><head><title>Product Title</title></head>
    <body>
        <time datetime="2024-03-15T12:00:00Z">Mar 15</time>
        <p>Product description.</p>
        <span class="price">$9.99</span>
    </body></html>
    """

    dummy_resp = DummyResponse(text=html)
    monkeypatch.setattr(crawler.requests, "get", lambda url, timeout=10: dummy_resp)

    result = crawler.crawl_price("http://example.com/product", source="Shop")
    assert result == {
        "title": "Product Title",
        "content": "Product description.",
        "source": "Shop",
        "published_at": "2024-03-15",
        "price": 9.99,
    }


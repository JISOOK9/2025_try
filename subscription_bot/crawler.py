"""Simple web crawler to fetch review content.

This module provides a basic example of fetching a web page and
extracting title and paragraph text using BeautifulSoup.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup


def crawl_review(url: str, source: str = "unknown") -> Dict[str, Any]:
    """Fetch ``url`` and extract a review-like JSON structure.

    Parameters
    ----------
    url:
        URL to crawl.
    source:
        Optional label for the source of the review.

    Returns
    -------
    dict
        A dictionary with ``title``, ``content``, ``source``, ``published_at``
        and ``price`` (always ``None`` for reviews) fields.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else ""
    content = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))

    return {
        "title": title,
        "content": content,
        "source": source,
        "published_at": datetime.utcnow().strftime("%Y-%m-%d"),
        "price": None,
    }


def crawl_news(url: str, source: str = "unknown") -> Dict[str, Any]:
    """Fetch ``url`` and extract news article information.

    Parameters
    ----------
    url:
        URL to crawl.
    source:
        Optional label for the source of the news article.

    Returns
    -------
    dict
        A dictionary with ``title``, ``content``, ``source``, ``published_at``
        and ``price`` (always ``None`` for news) fields.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else ""
    content = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
    time_tag = soup.find("time")
    if time_tag and time_tag.get("datetime"):
        published_at = time_tag.get("datetime").split("T")[0]
    else:
        published_at = datetime.utcnow().strftime("%Y-%m-%d")

    return {
        "title": title,
        "content": content,
        "source": source,
        "published_at": published_at,
        "price": None,
    }


def crawl_price(url: str, source: str = "unknown") -> Dict[str, Any]:
    """Fetch ``url`` and extract price information from a product page.

    Parameters
    ----------
    url:
        URL to crawl.
    source:
        Optional label for the source of the product.

    Returns
    -------
    dict
        A dictionary with ``title``, ``content``, ``source``, ``published_at``
        and ``price`` fields.
    """
    import re

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else ""
    content = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))

    time_tag = soup.find("time")
    if time_tag and time_tag.get("datetime"):
        published_at = time_tag.get("datetime").split("T")[0]
    else:
        published_at = datetime.utcnow().strftime("%Y-%m-%d")

    price = None
    price_elem = soup.find(attrs={"class": re.compile("price", re.I)}) or soup.find(
        attrs={"id": re.compile("price", re.I)}
    )
    if price_elem:
        price_text = price_elem.get_text(strip=True)
        match = re.search(r"[0-9]+(?:\.[0-9]+)?", price_text.replace(",", ""))
        if match:
            price = float(match.group())

    return {
        "title": title,
        "content": content,
        "source": source,
        "published_at": published_at,
        "price": price,
    }

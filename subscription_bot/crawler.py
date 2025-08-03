"""Simple web crawler to fetch review content.

This module provides a basic example of fetching a web page and
extracting title and paragraph text using BeautifulSoup.
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict

import requests
from bs4 import BeautifulSoup


def crawl_review(url: str, source: str = "unknown") -> Dict[str, str]:
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
        A dictionary with ``title``, ``content``, ``source`` and
        ``published_at`` fields.
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
    }

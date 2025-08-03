"""Simple text summarizer placeholder."""
from __future__ import annotations


def summarize(text: str, max_sentences: int = 3) -> str:
    """Return the first ``max_sentences`` from ``text``.

    This is a placeholder for an actual summarization model.
    """
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    summary = ". ".join(sentences[:max_sentences])
    if summary and not summary.endswith("."):
        summary += "."
    return summary

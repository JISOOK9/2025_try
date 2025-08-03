"""Sentiment analysis using VADER."""
from __future__ import annotations

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    """Return sentiment label (긍정/부정/중립) for ``text``."""
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "긍정"
    if compound <= -0.05:
        return "부정"
    return "중립"

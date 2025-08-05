"""Sentiment analysis utilities using both BERT and VADER models."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------------------------------------------------------------------
# BERT model setup
# ---------------------------------------------------------------------------

_tokenizer: AutoTokenizer | None = None
_model: AutoModelForSequenceClassification | None = None

# label mapping from model output index to Korean label
_LABEL_MAP = {0: "부정", 1: "중립", 2: "긍정"}


def load_model(checkpoint: str | None = None) -> Tuple[AutoTokenizer, AutoModelForSequenceClassification]:
    """Load a BERT sentiment model and tokenizer.

    Parameters
    ----------
    checkpoint:
        Optional local directory or model name to load. If ``None`` or the
        checkpoint does not exist, a pretrained sentiment analysis model is
        used instead.

    Returns
    -------
    Tuple[AutoTokenizer, AutoModelForSequenceClassification]
        The loaded tokenizer and model instances.
    """

    global _tokenizer, _model

    model_name = checkpoint or "cardiffnlp/twitter-roberta-base-sentiment"
    if checkpoint and not Path(checkpoint).exists():
        # Fallback to pretrained model when checkpoint is missing
        model_name = "cardiffnlp/twitter-roberta-base-sentiment"

    _tokenizer = AutoTokenizer.from_pretrained(model_name)
    _model = AutoModelForSequenceClassification.from_pretrained(model_name)

    return _tokenizer, _model


def analyze_sentiment(text: str) -> str:
    """Return sentiment label (긍정/부정/중립) for ``text`` using BERT."""

    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        load_model()

    assert _tokenizer is not None and _model is not None  # for type checkers

    inputs = _tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = _model(**inputs).logits
        label_id = int(torch.argmax(logits, dim=-1))

    return _LABEL_MAP.get(label_id, "중립")


# ---------------------------------------------------------------------------
# VADER sentiment for comparison
# ---------------------------------------------------------------------------

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment_vader(text: str) -> str:
    """Return sentiment label (긍정/부정/중립) for ``text`` using VADER."""

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "긍정"
    if compound <= -0.05:
        return "부정"
    return "중립"


__all__ = ["load_model", "analyze_sentiment", "analyze_sentiment_vader"]


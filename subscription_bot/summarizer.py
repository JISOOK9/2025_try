"""Korean text summarization using HuggingFace transformers.

This module lazily loads either a Pegasus or KoBART model for
summarization. Loading these models is heavy, so they are cached at the
module level and only loaded upon first use.
"""
from __future__ import annotations

from typing import Tuple

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

_MODEL_NAMES = [
    "hyunwoongko/pegasus-ko",  # Pegasus model fine-tuned for Korean summarization
    "gogamza/kobart-summarization",  # KoBART summarization model
]

_TOKENIZER = None
_MODEL = None


def _load_model() -> Tuple[AutoTokenizer, AutoModelForSeq2SeqLM]:
    """Load and cache a summarization model.

    Returns
    -------
    Tuple[AutoTokenizer, AutoModelForSeq2SeqLM]
        The tokenizer and model ready for inference.
    """
    global _TOKENIZER, _MODEL
    if _TOKENIZER is not None and _MODEL is not None:
        return _TOKENIZER, _MODEL

    last_error = None
    for name in _MODEL_NAMES:
        try:
            tokenizer = AutoTokenizer.from_pretrained(name)
            model = AutoModelForSeq2SeqLM.from_pretrained(name)
            model.eval()
            _TOKENIZER, _MODEL = tokenizer, model
            return tokenizer, model
        except Exception as exc:  # pragma: no cover - network/model issues
            last_error = exc
            _TOKENIZER, _MODEL = None, None
    raise RuntimeError("Failed to load a summarization model") from last_error


def summarize(text: str, max_length: int = 60, min_length: int = 5) -> str:
    """Summarize the input ``text`` using a pre-trained model.

    Parameters
    ----------
    text: str
        Input document to summarize.
    max_length: int, optional
        Maximum length of the summary in tokens.
    min_length: int, optional
        Minimum length of the summary in tokens.
    """
    tokenizer, model = _load_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        summary_ids = model.generate(
            **inputs, num_beams=4, max_length=max_length, min_length=min_length
        )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary.strip()

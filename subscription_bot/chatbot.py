"""High-level chatbot interface combining intent classification and responses."""
from __future__ import annotations

from typing import Optional

from .intent_classifier import predict_intent
from .response import generate_response


def answer(question: str, context: Optional[dict] = None) -> str:
    """Return chatbot answer for ``question`` using optional ``context``."""
    intent = predict_intent(question)
    return generate_response(intent, question, context)

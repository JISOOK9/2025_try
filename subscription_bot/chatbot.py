"""High-level chatbot interface combining intent classification and responses."""
from __future__ import annotations

from typing import Optional

from .intent_classifier import predict_intent
from .response import generate_response
from .embedding import embed_context, mask_personal_info


def answer(question: str, context: Optional[dict] = None) -> str:
    """Return chatbot answer for ``question`` using optional ``context``.

    The provided ``context`` is first sanitized to remove personal information
    and then embedded into a numeric vector. The embedding is injected into the
    context before being passed to the response generator, simulating an LLM
    prompt with contextual information.
    """
    context = context or {}
    sanitized = mask_personal_info(context)
    embedding = embed_context(sanitized)
    # Inject embedding into context for downstream LLM usage
    llm_context = dict(sanitized)
    llm_context["embedding"] = embedding

    intent = predict_intent(question)
    return generate_response(intent, question, llm_context)

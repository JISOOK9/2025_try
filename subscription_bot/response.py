"""Rule-based response generator with simple fallback."""
from __future__ import annotations

import re
from typing import Callable, Dict, Optional

from transformers import pipeline

RULES: Dict[str, Callable[[dict], str]] = {
    "조회": lambda ctx: "현재 구독 중인 상품은 {}입니다.".format(
        ", ".join(ctx.get("subscriptions", []) or ["없음"])
    ),
    "비교": lambda ctx: "비교 결과: 각 서비스마다 장단점이 있어요.",
    "추천": lambda ctx: "사용자님께는 {}를 추천합니다.".format(
        ctx.get("recommendation", "넷플릭스")
    ),
    "해지": lambda ctx: "구독 해지는 설정 > 구독관리에서 가능합니다.",
    "고민": lambda ctx: "고민이 되신다면 무료 체험을 먼저 이용해보세요.",
}


def _filter_pii(text: str) -> str:
    """Basic PII filtering for digits and emails."""
    if not text:
        return ""
    text = re.sub(r"[\w.%-]+@[\w.-]+\.[A-Za-z]{2,}", "<EMAIL>", text)
    text = re.sub(r"\d+", "<NUM>", text)
    return text


def generate_llm_response(
    intent: str, question: str, context: Optional[dict] = None
) -> str:
    """Generate response using an LLM with simple sanitisation.

    This function builds a prompt from the user's ``question`` and optional
    ``context`` after applying a minimal PII filter. It then queries a small
    language model via :func:`transformers.pipeline`. Any exception results in a
    safe fallback message.
    """

    context = context or {}
    sanitized_question = _filter_pii(question)
    sanitized_context = _filter_pii(str(context))
    prompt = f"사용자 질문: {sanitized_question}\n컨텍스트: {sanitized_context}\n답변:"
    try:
        generator = pipeline("text-generation", model="distilgpt2")
        result = generator(prompt, max_length=100, num_return_sequences=1)
        return result[0]["generated_text"].strip()
    except Exception:
        return "죄송해요. 아직 잘 모르겠어요."


def generate_response(intent: str, question: str, context: Optional[dict] = None) -> str:
    """Generate response based on ``intent`` and optional ``context``.

    If ``intent`` is not in predefined rules, an LLM-based response is used as
    fallback.
    """
    context = context or {}
    if intent in RULES:
        return RULES[intent](context)
    return generate_llm_response(intent, question, context)

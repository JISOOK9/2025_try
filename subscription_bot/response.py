"""Rule-based response generator with simple fallback."""
from __future__ import annotations

from typing import Callable, Dict, Optional

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


def generate_response(intent: str, question: str, context: Optional[dict] = None) -> str:
    """Generate response based on ``intent`` and optional ``context``.

    If ``intent`` is not in predefined rules, a fallback message is returned.
    """
    context = context or {}
    if intent in RULES:
        return RULES[intent](context)
    return "죄송해요. 아직 잘 모르겠어요."

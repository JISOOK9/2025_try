import pytest

from subscription_bot.intent_classifier import predict_intent
from subscription_bot.response import generate_response

from tests.utils import (
    build_confusion_matrix,
    save_confusion_matrix,
    calculate_fallback_rate,
    FALLBACK_MESSAGE,
)

SCENARIOS = [
    {"question": "내 구독 목록 알려줘", "intent": "조회", "context": {"subscriptions": ["넷플릭스", "디즈니+"]}},
    {"question": "구독 목록 좀 알려줄래?", "intent": "조회", "context": {"subscriptions": ["유튜브 프리미엄"]}},
    {"question": "현재 구독 목록을 알려줘.", "intent": "조회", "context": {"subscriptions": []}},
    {"question": "내 구독 서비스 목록 알려줘.", "intent": "조회", "context": {"subscriptions": ["티빙", "웨이브"]}},
    {"question": "넷플릭스랑 디즈니플러스 뭐가 달라?", "intent": "비교"},
    {"question": "디즈니플러스와 넷플릭스는 뭐가 다른가요?", "intent": "비교"},
    {"question": "넷플릭스 디즈니플러스 비교해줘", "intent": "비교"},
    {"question": "넷플릭스랑 디즈니플러스 비교 부탁해요", "intent": "비교"},
    {"question": "가성비 좋은 OTT 뭐 있어?", "intent": "추천", "context": {"recommendation": "왓챠"}},
    {"question": "가성비 좋은 OTT 추천해줘", "intent": "추천", "context": {"recommendation": "웨이브"}},
    {"question": "OTT 중 가성비 좋은 것 뭐야?", "intent": "추천", "context": {"recommendation": "쿠팡플레이"}},
    {"question": "가성비 괜찮은 OTT 알려줘", "intent": "추천"},
    {"question": "유튜브 프리미엄 해지하고 싶어요", "intent": "해지"},
    {"question": "유튜브 프리미엄 해지하고 싶습니다", "intent": "해지"},
    {"question": "유튜브 프리미엄을 해지하고 싶어요", "intent": "해지"},
    {"question": "프리미엄 유튜브 해지하고 싶어요", "intent": "해지"},
    {"question": "계속 써야 할지 고민이에요", "intent": "고민"},
    {"question": "계속 써야 할지 고민 중이야", "intent": "고민"},
    {"question": "이걸 계속 써야 할지 고민이에요", "intent": "고민"},
    {"question": "구독을 계속 써야 할지 고민이야", "intent": "고민"},
    {"question": "이건 잘 모르겠는 질문이야", "intent": "기타", "force_intent": "기타"},
]

EXPECTED_FRAGMENT = {
    "조회": "현재 구독 중인 상품은",
    "비교": "비교 결과",
    "추천": "추천합니다",
    "해지": "구독 해지는",
    "고민": "무료 체험",
    "기타": "죄송해요",
}


def test_scenarios(tmp_path):
    true_labels = []
    predicted_labels = []
    responses = []

    for sc in SCENARIOS:
        pred = predict_intent(sc["question"])
        predicted_labels.append(pred)
        true_labels.append(sc["intent"])

        intent_for_response = sc.get("force_intent", pred)
        response = generate_response(intent_for_response, sc["question"], sc.get("context"))
        responses.append(response)

        # Response validation
        assert EXPECTED_FRAGMENT[intent_for_response] in response

        if intent_for_response == "조회":
            subs = sc.get("context", {}).get("subscriptions", [])
            if subs:
                for s in subs:
                    assert s in response
            else:
                assert "없음" in response
        if intent_for_response == "추천":
            rec = sc.get("context", {}).get("recommendation", "넷플릭스")
            assert rec in response

        if sc["intent"] != "기타":
            assert pred == sc["intent"], f"Misclassified: {sc['question']}"
        else:
            assert FALLBACK_MESSAGE in response

    labels, cm = build_confusion_matrix(true_labels, predicted_labels)
    save_confusion_matrix(labels, cm, tmp_path / "confusion_matrix.csv")
    fallback_rate = calculate_fallback_rate(responses)

    print("Labels:", labels)
    print(cm)
    print(f"Fallback rate: {fallback_rate:.2%}")

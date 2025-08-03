from subscription_bot.intent_classifier import predict_intent


def test_predict_intent():
    assert predict_intent("내 구독 목록 알려줘") == "조회"
    assert predict_intent("유튜브 프리미엄 해지하고 싶어요") == "해지"

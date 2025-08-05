from subscription_bot.response import generate_response


def test_rule_response():
    ctx = {"subscriptions": ["넷플릭스"]}
    resp = generate_response("조회", "내 구독 알려줘", ctx)
    assert "넷플릭스" in resp


def test_fallback(monkeypatch):
    monkeypatch.setattr(
        "subscription_bot.response.generate_llm_response",
        lambda intent, question, context: "죄송해요",
    )
    resp = generate_response("기타", "모르는 질문", {})
    assert "죄송해요" in resp

from subscription_bot.data.service import build_user_context
import subscription_bot.data.internal as internal
import subscription_bot.data.external as external


def test_build_user_context_merges_internal_and_external(monkeypatch):
    def fake_internal(user_id):
        return {"user_id": user_id, "subscriptions": ["넷플릭스"]}

    def fake_external(user_id):
        return {"subscriptions": ["디즈니+"], "reviews": [{"title": "A"}]}

    monkeypatch.setattr(internal, "get_user_info", fake_internal)
    monkeypatch.setattr(external, "crawl_user_data", fake_external)

    ctx = build_user_context(99)
    assert ctx["user_id"] == 99
    assert ctx["subscriptions"] == ["넷플릭스", "디즈니+"]
    assert ctx["reviews"] == [{"title": "A"}]

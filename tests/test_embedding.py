from subscription_bot.embedding import embed_context, mask_personal_info


def test_mask_personal_info_removes_pii():
    data = {
        "email": "user@example.com",
        "user_id": "u123",
        "subscriptions": ["넷플릭스", "디즈니"],
        "payment_amount": 12000,
    }
    sanitized = mask_personal_info(data)
    assert "email" not in sanitized
    assert "user_id" not in sanitized
    assert sanitized["subscriptions"] == ["넷플릭스", "디즈니"]


def test_embed_context_vectorizes_data():
    data = {
        "email": "user@example.com",
        "subscriptions": ["넷플릭스", "디즈니"],
        "payment_amount": 15000,
    }
    vector = embed_context(data)
    # payment amount should come first after sorting feature names
    assert vector[0] == 15000.0
    # remaining features correspond to subscriptions and are binary
    assert vector[1:] == [1.0, 1.0]

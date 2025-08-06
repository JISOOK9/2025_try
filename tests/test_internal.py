import subscription_bot.data.internal as internal


def test_get_user_subscription_state():
    backend = internal.InMemoryStorage(
        subscriptions={"user123": {"status": "active", "product_id": "prod1"}}
    )
    internal.set_storage_backend(backend)
    result = internal.get_user_subscription_state("user123")
    assert result == {"status": "active", "product_id": "prod1"}
    assert isinstance(result, dict)


def test_get_payment_history():
    backend = internal.InMemoryStorage(
        payments={
            "user123": [
                {"amount": 10, "currency": "USD"},
                {"amount": 5, "currency": "USD"},
            ]
        }
    )
    internal.set_storage_backend(backend)
    history = internal.get_payment_history("user123")
    assert isinstance(history, list)
    assert history[0]["amount"] == 10
    assert history[1]["currency"] == "USD"


def test_get_product_metadata():
    backend = internal.InMemoryStorage(
        products={"prod1": {"name": "Pro Plan", "price": 10.0}}
    )
    internal.set_storage_backend(backend)
    metadata = internal.get_product_metadata("prod1")
    assert metadata == {"name": "Pro Plan", "price": 10.0}
    assert isinstance(metadata, dict)

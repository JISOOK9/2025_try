import os

import pytest
from sqlalchemy import text

# set DB URL before importing modules that use it
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from subscription_bot.db import get_engine  # noqa: E402
from subscription_bot.response import generate_response  # noqa: E402


@pytest.fixture(scope="module")
def setup_db():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE subscriptions (user_id INTEGER, name TEXT)"))
        conn.execute(
            text(
                "INSERT INTO subscriptions (user_id, name) VALUES (1, '넷플릭스'), (1, '디즈니+')"
            )
        )
    yield


def test_db_lookup_updates_context(setup_db):
    ctx = {"user_id": 1}
    resp = generate_response("조회", "내 구독 알려줘", ctx)
    assert "넷플릭스" in resp and "디즈니+" in resp
    assert ctx["subscriptions"] == ["넷플릭스", "디즈니+"]

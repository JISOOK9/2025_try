from fastapi.testclient import TestClient

from subscription_bot.api import app


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_chat(monkeypatch):
    def fake_answer(question, context=None):
        assert question == "테스트"
        return "응답"

    monkeypatch.setattr("subscription_bot.chatbot.answer", fake_answer)

    resp = client.post("/chat", json={"question": "테스트"})
    assert resp.status_code == 200
    assert resp.json() == {"answer": "응답"}


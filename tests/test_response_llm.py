import pytest

from subscription_bot.response import generate_response


def test_llm_fallback(monkeypatch):
    """Unknown intents should trigger the LLM based fallback."""
    captured = {}

    def fake_pipeline(task, model):
        def _generate(prompt, max_length=100, num_return_sequences=1):
            captured["prompt"] = prompt
            return [{"generated_text": "llm output"}]
        return _generate

    monkeypatch.setattr("subscription_bot.response.pipeline", fake_pipeline)

    result = generate_response(
        "알수없음", "전화번호는 01012345678", {"email": "user@example.com"}
    )

    assert result == "llm output"
    assert "<NUM>" in captured["prompt"]
    assert "<EMAIL>" in captured["prompt"]

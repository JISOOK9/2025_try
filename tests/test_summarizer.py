from subscription_bot.summarizer import summarize


def test_summary_short_text_is_not_longer_than_input():
    text = "안녕하세요. 오늘은 날씨가 참 좋습니다. 산책을 가고 싶네요."
    summary = summarize(text)
    assert isinstance(summary, str)
    assert summary
    assert len(summary) <= len(text)


def test_summarize_is_deterministic_with_cache():
    text = "간단한 테스트 문장입니다. 요약이 동일하게 나와야 합니다."
    first = summarize(text)
    second = summarize(text)
    assert first == second

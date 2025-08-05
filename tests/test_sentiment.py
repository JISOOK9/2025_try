from subscription_bot.sentiment import analyze_sentiment_vader


def test_sentiment_vader():
    assert analyze_sentiment_vader("I love this service") == "긍정"
    assert analyze_sentiment_vader("I hate this service") == "부정"

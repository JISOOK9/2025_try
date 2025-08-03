from subscription_bot.sentiment import analyze_sentiment


def test_sentiment():
    assert analyze_sentiment("I love this service") == "긍정"
    assert analyze_sentiment("I hate this service") == "부정"

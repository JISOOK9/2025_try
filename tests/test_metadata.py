from subscription_bot.metadata import tag_metadata


def test_tag_metadata():
    text = "아마존 프라임은 월 5달러에 무료 배송 혜택을 제공합니다."
    result = tag_metadata(text)
    assert result["상품명"] == "아마존 프라임"
    assert result["가격"] == ["5달러"]
    assert result["혜택"] == ["무료 배송"]

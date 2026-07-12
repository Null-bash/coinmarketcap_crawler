import pytest

from scrape.scrape.spiders.converter import ConvertSpider

def test__init__():
    from_coin = "btc"
    to_coin = "rth"
    spider = ConvertSpider(from_coin=from_coin, to_coin=to_coin)
    assert spider.from_coin == from_coin
    assert spider.to_coin == to_coin
    assert len(spider.start_urls) == 1
    assert spider.start_urls == [
        "https://coinmarketcap.com/converter/"
    ]

def test__init__raises_value_error_if_from_coin_is_none():
    with pytest.raises(ValueError):
        ConvertSpider(from_coin=None, to_coin="rth")

def test__init__raises_value_error_if_to_coin_is_none():
    with pytest.raises(ValueError):
        ConvertSpider(from_coin="btc", to_coin=None)


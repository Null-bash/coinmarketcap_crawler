"""
Tests for ConvertSpider.

Covers:
- Initialization
- Input validation
- Start request generation
- Coin selection
- Parsing converter results
"""

import pytest

from scrape.scrape.spiders.converter import ConvertSpider

# ============================================================================
# __init__
#
# Tests:
# - Valid initialization
# - Required arguments
# - Invalid coin symbols
# ============================================================================

def test_init():
    spider = ConvertSpider(
        from_coin="btc",
        to_coin="eth",
    )

    assert spider.from_coin == "btc"
    assert spider.to_coin == "eth"
    assert spider.start_urls == [
        "https://coinmarketcap.com/converter/"
    ]


def test_init_raises_if_from_coin_is_none():
    with pytest.raises(ValueError):
        ConvertSpider(
            from_coin=None,
            to_coin="eth",
        )


def test_init_raises_if_to_coin_is_none():
    with pytest.raises(ValueError):
        ConvertSpider(
            from_coin="btc",
            to_coin=None,
        )


def test_init_raises_if_both_coins_are_none():
    with pytest.raises(ValueError):
        ConvertSpider(
            from_coin=None,
            to_coin=None,
        )


def test_init_raises_if_from_coin_is_numeric():
    with pytest.raises(ValueError):
        ConvertSpider(
            from_coin="123",
            to_coin="eth",
        )


def test_init_raises_if_to_coin_is_numeric():
    with pytest.raises(ValueError):
        ConvertSpider(
            from_coin="btc",
            to_coin="123",
        )


# ============================================================================
# start
#
# Tests:
# - Request generation
# - Callback assignment
# - Playwright metadata
# ============================================================================

@pytest.mark.asyncio
async def test_start():
    spider = ConvertSpider(
        from_coin="btc",
        to_coin="eth",
    )

    requests = [request async for request in spider.start()]

    assert len(requests) == 1

    request = requests[0]

    assert request.url == "https://coinmarketcap.com/converter/"
    assert request.callback == spider.parse

    assert request.meta["playwright"] is True
    assert request.meta["playwright_include_page"] is True
    assert (
        request.meta["playwright_page_goto_kwargs"]["wait_until"]
        == "networkidle"
    )


# ============================================================================
# select_coin
#
# Tests:
# - Valid coin selection
# - Unknown coin handling
# ============================================================================


@pytest.mark.asyncio
async def test_select_coin(fake_page):
    spider = ConvertSpider(
        from_coin="btc",
        to_coin="eth",
    )

    await spider.select_coin(
        fake_page,
        spider.FROM_INPUT,
        "btc",
    )

    fake_page.locator.assert_any_call(
        spider.FROM_INPUT
    )


@pytest.mark.asyncio
async def test_select_coin_raises_for_unknown_coin(fake_page):
    spider = ConvertSpider(
        from_coin="abcdef",
        to_coin="eth",
    )

    options = fake_page.locator(
        spider.OPTION_SELECTOR
    )

    options.count.return_value = 0

    with pytest.raises(ValueError):
        await spider.select_coin(
            fake_page,
            spider.FROM_INPUT,
            "abcdef",
        )


# ============================================================================
# parse
#
# Tests:
# - Extract conversion result
# - Close Playwright page
# ============================================================================

@pytest.mark.asyncio
async def test_parse(fake_response, fake_page):
    spider = ConvertSpider(
        from_coin="btc",
        to_coin="eth",
    )

    items = [
        item async for item in spider.parse(fake_response)
    ]

    assert len(items) == 1

    item = items[0]

    assert "FromCoin" in item
    assert "ToCoin" in item

    fake_page.content.assert_awaited_once()
    fake_page.close.assert_awaited_once()
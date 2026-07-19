"""
Tests for SymbolSearchSpider.

Covers:
- Initialization
- Symbol validation
- URL generation
- Start request generation
- Parsing coin information
"""

import pytest

from scrape.scrape.spiders.symbol_search import SymbolSearchSpider

# ============================================================================
# __init__
#
# Tests:
# - Valid initialization
# - Symbol validation
# - URL lookup
# - URL generation
# ============================================================================

def test_init():
    spider = SymbolSearchSpider(symbol="btc")

    assert spider.start_urls == [
        "https://coinmarketcap.com/currencies/bitcoin/"
    ]


def test_init_raises_if_symbol_is_none():
    with pytest.raises(ValueError):
        SymbolSearchSpider(symbol=None)


def test_init_raises_lookup_error(mocker):
    mocker.patch(
        "scrape.scrape.spiders.symbol_search.get_url_by_sym",
        return_value=None,
    )

    with pytest.raises(
        LookupError,
        match="Coin 'abc' not found",
    ):
        SymbolSearchSpider(symbol="abc")


def test_init_sets_start_url(mocker):
    mocker.patch(
        "scrape.scrape.spiders.symbol_search.get_url_by_sym",
        return_value="/currencies/bitcoin/",
    )

    spider = SymbolSearchSpider(symbol="btc")

    assert spider.start_urls == [
        "https://coinmarketcap.com/currencies/bitcoin/"
    ]


def test_init_accepts_uppercase_symbol():
    spider = SymbolSearchSpider(symbol="BTC")

    assert spider.start_urls == [
        "https://coinmarketcap.com/currencies/bitcoin/"
    ]


def test_init_calls_get_url_by_sym_with_uppercase(mocker):
    mocked = mocker.patch(
        "scrape.scrape.spiders.symbol_search.get_url_by_sym",
        return_value="/currencies/bitcoin/",
    )

    SymbolSearchSpider(symbol="btc")

    mocked.assert_called_once_with("BTC")


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
    spider = SymbolSearchSpider(symbol="btc")

    requests = [request async for request in spider.start()]

    assert len(requests) == 1

    request = requests[0]

    assert request.url == spider.start_urls[0]
    assert request.callback == spider.parse

    assert request.meta["playwright"] is True
    assert request.meta["playwright_include_page"] is True


# ============================================================================
# parse
#
# Tests:
# - Extract coin information
# - Handle empty HTML
# - Close Playwright page
# ============================================================================

@pytest.mark.asyncio
async def test_parse(fake_response, fake_page):
    spider = SymbolSearchSpider(symbol="btc")

    fake_page.content.return_value = """
    <html>
        <span data-role="coin-name">Bitcoin</span>
        <span data-test="text-cdp-price-display">$117,000</span>
    </html>
    """

    items = [
        item async for item in spider.parse(fake_response)
    ]

    assert len(items) == 1

    item = items[0]

    assert item["Name"] == "Bitcoin"
    assert item["Price"] == "$117,000"

    fake_page.content.assert_awaited_once()


@pytest.mark.asyncio
async def test_parse_closes_page(fake_response, fake_page):
    spider = SymbolSearchSpider(symbol="btc")

    fake_page.content.return_value = """
    <html>
        <span data-role="coin-name">Bitcoin</span>
        <span data-test="text-cdp-price-display">$117,000</span>
    </html>
    """

    _ = [item async for item in spider.parse(fake_response)]

    fake_page.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_parse_returns_none_when_html_is_empty(
    fake_response,
    fake_page,
):
    spider = SymbolSearchSpider(symbol="btc")

    fake_page.content.return_value = "<html></html>"

    items = [
        item async for item in spider.parse(fake_response)
    ]

    assert len(items) == 1
    assert items[0]["Name"] is None
    assert items[0]["Price"] is None
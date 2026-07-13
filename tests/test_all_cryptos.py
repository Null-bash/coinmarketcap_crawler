"""
Tests for AllCryptoSpider.

Covers:
- Initialization
- Input validation
- Start request generation
- Parsing cryptocurrency data
"""

import pytest

from scrapy_playwright.page import PageMethod

from scrape.scrape.spiders.all_cryptos import AllCryptoSpider


# ============================================================================
# __init__
#
# Tests:
# - Default values
# - Valid initialization
# - Input validation
# - URL generation
# ============================================================================

def test_init():
    spider = AllCryptoSpider(to_page=3)

    assert spider.to_page == 3
    assert spider.start_urls == [
        "https://coinmarketcap.com/?page=1",
        "https://coinmarketcap.com/?page=2",
        "https://coinmarketcap.com/?page=3",
    ]


def test_init_accepts_string_number():
    spider = AllCryptoSpider(to_page="5")

    assert spider.to_page == 5


def test_init_default_value():
    spider = AllCryptoSpider()

    assert spider.to_page == 81
    assert len(spider.start_urls) == 81


def test_init_raises_if_not_integer():
    with pytest.raises(ValueError):
        AllCryptoSpider(to_page="abc")


def test_init_raises_if_none():
    with pytest.raises(ValueError):
        AllCryptoSpider(to_page=None)


def test_init_raises_if_zero():
    with pytest.raises(ValueError):
        AllCryptoSpider(to_page=0)


def test_init_raises_if_negative():
    with pytest.raises(ValueError):
        AllCryptoSpider(to_page=-5)


def test_start_urls_are_generated_correctly():
    spider = AllCryptoSpider(to_page=2)

    assert len(spider.start_urls) == 2
    assert spider.start_urls[0] == "https://coinmarketcap.com/?page=1"
    assert spider.start_urls[1] == "https://coinmarketcap.com/?page=2"


# ============================================================================
# start
#
# Tests:
# - Request generation
# - Playwright metadata
# - Page methods
# ============================================================================

@pytest.mark.asyncio
async def test_start():
    spider = AllCryptoSpider(to_page=2)

    requests = [request async for request in spider.start()]

    assert len(requests) == 2

    request = requests[0]

    assert request.url == "https://coinmarketcap.com/?page=1"

    assert request.meta["playwright"] is True
    assert request.meta["playwright_include_page"] is True

    methods = request.meta["playwright_page_methods"]

    assert len(methods) == 2
    assert isinstance(methods[0], PageMethod)
    assert isinstance(methods[1], PageMethod)


# ============================================================================
# parse
#
# Tests:
# - Item extraction
# - Empty table
# - Playwright interactions
# ============================================================================

@pytest.mark.asyncio
async def test_parse_returns_items(fake_page, fake_response):
    spider = AllCryptoSpider()

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody>
        <tr>
          <td>
            <a href="/currencies/bitcoin/">
              <p class="coin-item-name">Bitcoin</p>
            </a>
          </td>
          <td>
            <p class="coin-item-symbol">BTC</p>
          </td>
        </tr>

        <tr>
          <td>
            <a href="/currencies/ethereum/">
              <p class="coin-item-name">Ethereum</p>
            </a>
          </td>
          <td>
            <p class="coin-item-symbol">ETH</p>
          </td>
        </tr>
      </tbody>
    </table>
    """

    items = [item async for item in spider.parse(fake_response)]

    assert len(items) == 2

    assert items[0]["Name"] == "Bitcoin"
    assert items[0]["Symbol"] == "BTC"
    assert items[0]["web_path"] == "/currencies/bitcoin/"

    assert items[1]["Name"] == "Ethereum"
    assert items[1]["Symbol"] == "ETH"
    assert items[1]["web_path"] == "/currencies/ethereum/"


@pytest.mark.asyncio
async def test_parse_empty_table(fake_page, fake_response):
    spider = AllCryptoSpider()

    fake_page.content.return_value = """
    <table class="cmc-table">
        <tbody></tbody>
    </table>
    """

    items = [item async for item in spider.parse(fake_response)]

    assert items == []


@pytest.mark.asyncio
async def test_parse_calls_page_methods(fake_page, fake_response):
    spider = AllCryptoSpider()

    fake_page.content.return_value = """
    <table class="cmc-table">
        <tbody></tbody>
    </table>
    """

    _ = [item async for item in spider.parse(fake_response)]

    fake_page.content.assert_awaited_once()
    fake_page.close.assert_awaited_once()
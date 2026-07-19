"""
Tests for TopPriceSpider.

Covers:
- Initialization
- Input validation
- Start request generation
- Parsing top-priced cryptocurrencies
"""

import pytest

from scrape.scrape.spiders.top_price import TopPriceSpider

# ============================================================================
# __init__
#
# Tests:
# - Valid initialization
# - Default and boundary values
# - Input validation
# ============================================================================

def test_init():
    spider = TopPriceSpider(number_of_coins=10)

    assert spider.number_of_coins == 10
    assert spider.start_urls == [
        "https://coinmarketcap.com"
    ]


def test_init_accepts_string_number():
    spider = TopPriceSpider(number_of_coins="25")

    assert spider.number_of_coins == 25


def test_init_accepts_minimum():
    spider = TopPriceSpider(number_of_coins=1)

    assert spider.number_of_coins == 1


def test_init_accepts_maximum():
    spider = TopPriceSpider(number_of_coins=100)

    assert spider.number_of_coins == 100


def test_init_raises_if_less_than_one():
    with pytest.raises(ValueError):
        TopPriceSpider(number_of_coins=0)


def test_init_raises_if_greater_than_100():
    with pytest.raises(ValueError):
        TopPriceSpider(number_of_coins=101)


def test_init_raises_if_not_a_number():
    with pytest.raises(ValueError):
        TopPriceSpider(number_of_coins="abc")


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
    spider = TopPriceSpider(number_of_coins=10)

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
# - Extract items
# - Respect number_of_coins limit
# - Handle empty table
# - Verify Playwright interactions
# ============================================================================

@pytest.mark.asyncio
async def test_parse_returns_items(fake_page, fake_response):
    spider = TopPriceSpider(number_of_coins=2)

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody>
        <tr>
          <td><p class="coin-item-name">Bitcoin</p></td>
          <td><p class="coin-item-symbol">BTC</p></td>
          <td></td>
          <td><span>$100000</span></td>
        </tr>

        <tr>
          <td><p class="coin-item-name">Ethereum</p></td>
          <td><p class="coin-item-symbol">ETH</p></td>
          <td></td>
          <td><span>$5000</span></td>
        </tr>
      </tbody>
    </table>
    """

    items = [item async for item in spider.parse(fake_response)]

    assert len(items) == 2

    assert items[0]["Name"] == "Bitcoin"
    assert items[0]["Symbol"] == "BTC"
    assert items[0]["Price"] == "$100000"

    assert items[1]["Name"] == "Ethereum"
    assert items[1]["Symbol"] == "ETH"
    assert items[1]["Price"] == "$5000"


@pytest.mark.asyncio
async def test_parse_limits_number_of_coins(fake_page, fake_response):
    spider = TopPriceSpider(number_of_coins=1)

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody>
        <tr>
          <td><p class="coin-item-name">Bitcoin</p></td>
          <td><p class="coin-item-symbol">BTC</p></td>
          <td></td>
          <td><span>$100000</span></td>
        </tr>

        <tr>
          <td><p class="coin-item-name">Ethereum</p></td>
          <td><p class="coin-item-symbol">ETH</p></td>
          <td></td>
          <td><span>$5000</span></td>
        </tr>
      </tbody>
    </table>
    """

    items = [item async for item in spider.parse(fake_response)]

    assert len(items) == 1


@pytest.mark.asyncio
async def test_parse_empty_table(fake_page, fake_response):
    spider = TopPriceSpider(number_of_coins=10)

    fake_page.content.return_value = """
    <table class="cmc-table">
        <tbody></tbody>
    </table>
    """

    items = [item async for item in spider.parse(fake_response)]

    assert items == []


@pytest.mark.asyncio
async def test_parse_calls_playwright_methods(fake_page, fake_response):
    spider = TopPriceSpider(number_of_coins=1)

    _ = [item async for item in spider.parse(fake_response)]

    fake_page.content.assert_awaited_once()
    fake_page.wait_for_timeout.assert_awaited_once_with(2000)

    fake_page.get_by_role.assert_any_call("button", name="Filters")
    fake_page.get_by_role.assert_any_call("button", name="Apply")
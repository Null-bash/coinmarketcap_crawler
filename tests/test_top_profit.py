"""
Tests for the TopProfitSpider.

Covered functionality:
- Spider initialization and input validation.
- Request generation in `start()`.
- Parsing the top profit table.
- Playwright interactions during parsing.
"""

import pytest

from scrape.scrape.spiders.top_profit import TopProfitSpider, tdomain_to_num

# ============================================================================
# __init__
# ============================================================================

def test_init():
    """Initialize the spider with valid arguments."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=10,
    )

    assert spider.tdomain_num == tdomain_to_num["24h"]
    assert spider.number_of_coins == 10
    assert spider.start_urls == [
        "https://coinmarketcap.com"
    ]


def test_init_accepts_string_number():
    """Accept numeric strings for number_of_coins."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins="25",
    )

    assert spider.number_of_coins == 25


def test_init_accepts_minimum_number():
    """Accept the minimum allowed number of coins."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=1,
    )

    assert spider.number_of_coins == 1


def test_init_accepts_maximum_number():
    """Accept the maximum allowed number of coins."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=100,
    )

    assert spider.number_of_coins == 100


def test_init_raises_if_tdomain_missing():
    """Raise ValueError when time domain is missing."""
    with pytest.raises(ValueError):
        TopProfitSpider(
            tdomain=None,
            number_of_coins=10,
        )


def test_init_raises_if_tdomain_invalid():
    """Raise ValueError for an unsupported time domain."""
    with pytest.raises(ValueError):
        TopProfitSpider(
            tdomain="abc",
            number_of_coins=10,
        )


def test_init_raises_if_number_too_small():
    """Raise ValueError when number_of_coins is below the limit."""
    with pytest.raises(ValueError):
        TopProfitSpider(
            tdomain="24h",
            number_of_coins=0,
        )


def test_init_raises_if_number_too_large():
    """Raise ValueError when number_of_coins exceeds the limit."""
    with pytest.raises(ValueError):
        TopProfitSpider(
            tdomain="24h",
            number_of_coins=101,
        )


def test_init_raises_if_number_not_numeric():
    """Raise ValueError when number_of_coins is not numeric."""
    with pytest.raises(ValueError):
        TopProfitSpider(
            tdomain="24h",
            number_of_coins="abc",
        )


# ============================================================================
# start()
# ============================================================================

@pytest.mark.asyncio
async def test_start():
    """Generate the expected Playwright request."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=10,
    )

    requests = [
        request async for request in spider.start()
    ]

    assert len(requests) == 1

    request = requests[0]

    assert request.url == spider.start_urls[0]
    assert request.callback == spider.parse

    assert request.meta["playwright"] is True
    assert request.meta["playwright_include_page"] is True
    assert (
        request.meta["playwright_page_goto_kwargs"]["wait_until"]
        == "domcontentloaded"
    )


# ============================================================================
# parse()
# ============================================================================

@pytest.mark.asyncio
async def test_parse_returns_items(fake_page, fake_response):
    """Extract coin information from the table."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=2,
    )

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody>
        <tr>
          <td><p class="coin-item-name">Bitcoin</p></td>
          <td><p class="coin-item-symbol">BTC</p></td>
          <td></td>
          <td><span>$100000</span></td>
          <td></td>
          <td><span>+5%</span></td>
        </tr>

        <tr>
          <td><p class="coin-item-name">Ethereum</p></td>
          <td><p class="coin-item-symbol">ETH</p></td>
          <td></td>
          <td><span>$5000</span></td>
          <td></td>
          <td><span>+3%</span></td>
        </tr>
      </tbody>
    </table>
    """

    items = [
        item async for item in spider.parse(fake_response)
    ]

    assert len(items) == 2

    assert items[0]["Name"] == "Bitcoin"
    assert items[0]["Symbol"] == "BTC"
    assert items[0]["Price"] == "$100000"
    assert items[0]["Price_Change"] == "+5%"

    assert items[1]["Name"] == "Ethereum"
    assert items[1]["Symbol"] == "ETH"
    assert items[1]["Price"] == "$5000"
    assert items[1]["Price_Change"] == "+3%"


@pytest.mark.asyncio
async def test_parse_limits_number_of_coins(
    fake_page,
    fake_response,
):
    """Return only the requested number of coins."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=1,
    )

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody>
        <tr>
          <td><p class="coin-item-name">Bitcoin</p></td>
          <td><p class="coin-item-symbol">BTC</p></td>
          <td></td>
          <td><span>$100000</span></td>
          <td></td>
          <td><span>+5%</span></td>
        </tr>

        <tr>
          <td><p class="coin-item-name">Ethereum</p></td>
          <td><p class="coin-item-symbol">ETH</p></td>
          <td></td>
          <td><span>$5000</span></td>
          <td></td>
          <td><span>+3%</span></td>
        </tr>
      </tbody>
    </table>
    """

    items = [
        item async for item in spider.parse(fake_response)
    ]

    assert len(items) == 1


@pytest.mark.asyncio
async def test_parse_empty_table(
    fake_page,
    fake_response,
):
    """Return an empty list when the table contains no rows."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=10,
    )

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody></tbody>
    </table>
    """

    items = [
        item async for item in spider.parse(fake_response)
    ]

    assert items == []


@pytest.mark.asyncio
async def test_parse_calls_playwright_methods(
    fake_page,
    fake_response,
):
    """Call the expected Playwright methods during parsing."""
    spider = TopProfitSpider(
        tdomain="24h",
        number_of_coins=1,
    )

    fake_page.content.return_value = """
    <table class="cmc-table">
      <tbody>
        <tr>
          <td><p class="coin-item-name">Bitcoin</p></td>
          <td><p class="coin-item-symbol">BTC</p></td>
          <td></td>
          <td><span>$100000</span></td>
          <td></td>
          <td><span>+5%</span></td>
        </tr>
      </tbody>
    </table>
    """

    _ = [
        item async for item in spider.parse(fake_response)
    ]

    fake_page.content.assert_awaited_once()
    fake_page.wait_for_timeout.assert_awaited_once_with(2000)

    fake_page.get_by_role.assert_any_call(
        "button",
        name="Filters",
    )
    fake_page.get_by_role.assert_any_call(
        "button",
        name="Apply",
    )
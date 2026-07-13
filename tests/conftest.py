"""
Shared pytest fixtures.

Provides mocked Playwright page and Scrapy response objects
for testing spiders without opening a real browser.
"""

import pytest

from unittest.mock import AsyncMock, MagicMock
from scrapy.http import HtmlResponse, Request


@pytest.fixture
def fake_page():
    """Return a mocked Playwright page."""

    page = MagicMock()

    page.content = AsyncMock(return_value="<html></html>")
    page.close = AsyncMock()
    page.wait_for_timeout = AsyncMock()

    # Generic locator
    locator = MagicMock()
    locator.wait_for = AsyncMock()
    locator.fill = AsyncMock()
    locator.click = AsyncMock()
    locator.locator.return_value = locator
    locator.nth.return_value = locator

    # Coin options list
    options = MagicMock()
    options.count = AsyncMock(return_value=1)
    options.nth.return_value = locator

    def locator_side_effect(selector):
        if "cmc-select__option" in selector:
            return options
        return locator

    page.locator.side_effect = locator_side_effect

    # Playwright buttons
    button = MagicMock()
    button.wait_for = AsyncMock()
    button.click = AsyncMock()

    page.get_by_role.return_value = button

    return page


@pytest.fixture
def fake_response(fake_page):
    """Return a mocked Scrapy response containing the fake page."""

    request = Request(
        url="https://coinmarketcap.com/converter/",
        meta={"playwright_page": fake_page},
    )

    return HtmlResponse(
        url=request.url,
        request=request,
        body="",
        encoding="utf-8",
    )
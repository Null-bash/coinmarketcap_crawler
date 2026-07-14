import scrapy
from scrapy_playwright.page import PageMethod
from scrape.utils.all_crypto import get_url_by_sym


class SymbolSearchSpider(scrapy.Spider):
    """
    Search for a cryptocurrency by its symbol and extract
    basic information from its CoinMarketCap page.
    """

    name = "symbol_search"
    allowed_domains = ["coinmarketcap.com"]

    def __init__(self, symbol=None, *args, **kwargs):
        """
        Validate the symbol and build the target CoinMarketCap URL.
        """
        super().__init__(*args, **kwargs)

        if not symbol:
            raise ValueError("symbol is required")

        coin_url = get_url_by_sym(symbol.upper())

        if coin_url is None:
            raise LookupError(f"Coin '{symbol}' not found")

        self.start_urls = [
            "https://coinmarketcap.com" + coin_url
        ]

    async def start(self):
        """
        Send the initial Playwright request.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    # "playwright_page_goto_kwargs": {
                    #     "wait_until": "domcontentloaded",
                    # },
                },
                callback=self.parse,
            )

    async def parse(self, response):
        """
        Wait for the page to load, then extract the coin name
        and current price.
        """
        page = response.meta["playwright_page"]

        html = await page.content()

        await page.locator(
            'xpath=//span[@data-test="text-cdp-price-display"]'
        ).nth(0).wait_for()

        response = response.replace(body=html)

        yield {
            "Name": response.xpath(
                '//span[@data-role="coin-name"]/text()'
            ).get(),

            "Price": response.xpath(
                '//span[@data-test="text-cdp-price-display"]/text()'
            ).get(),
        }

        await page.close()
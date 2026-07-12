import scrapy
from scrapy_playwright.page import PageMethod


tdomain_to_num = {
    "1h": 5,
    "24h": 6,
    "7d": 7,
}


class TopProfitSpider(scrapy.Spider):
    name = "top_profit"
    allowed_domains = ["coinmarketcap.com"]

    def __init__(self, tdomain, number_of_coins=10, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not tdomain:
            raise ValueError("tdomain is required")

        self.tdomain_num = tdomain_to_num.get(tdomain)

        if self.tdomain_num is None:
            raise ValueError(f"Invalid time domain: '{tdomain}'")

        self.number_of_coins = int(number_of_coins)

        if not (1 <= self.number_of_coins <= 100):
            raise ValueError("number_of_coins must be between 1 and 100.")

        self.start_urls = [
            "https://coinmarketcap.com"
        ]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_goto_kwargs": {
                        "wait_until": "domcontentloaded",
                    },
                },
                callback=self.parse,
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        btn = page.get_by_role("button", name="Filters")
        await btn.wait_for()
        await btn.click()

        loc = page.locator(
            'xpath=//div[contains(@class,"form-item")]'
        ).nth(0)
        await loc.wait_for()
        await loc.locator(
            'xpath=.//div[@data-role="select-trigger"]'
        ).click()

        loc = page.locator(
            'xpath=//div[@data-role="pp-item"]/div/div'
        ).nth(3)
        await loc.wait_for()
        await loc.click()

        await page.get_by_role("button", name="Apply").click()

        await page.locator(
            'xpath=//th[contains(@class,"stickyTop")]'
        ).nth(self.tdomain_num - 1).click()

        await page.wait_for_timeout(2000)

        html = await page.content()
        response = response.replace(body=html)

        for cursor in response.xpath(
            '//table[contains(@class,"cmc-table")]//tbody[1]//tr'
        )[:self.number_of_coins]:
            yield {
                "Name": cursor.xpath(
                    './/p[contains(@class,"coin-item-name")]/text()'
                    ' | '
                    './/a//span[2]/text()'
                ).get(),

                "Symbol": cursor.xpath(
                    './/p[contains(@class,"coin-item-symbol")]/text()'
                    ' | '
                    './/span[contains(@class,"crypto-symbol")]/text()'
                ).get(),

                "Price": cursor.xpath(
                    './/td[4]//span/text()'
                ).get(),

                "Price_Change": cursor.xpath(
                    f'.//td[{self.tdomain_num}]//span/text()'
                ).get(),
            }

        await page.close()
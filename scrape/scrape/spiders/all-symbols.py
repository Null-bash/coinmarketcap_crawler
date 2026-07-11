import scrapy
from scrapy_playwright.page import PageMethod
from scrape.utils.script import scrolling_script


class AllCoinsSpider(scrapy.Spider):
    name = "all_coins"
    allowed_domains = ["coinmarketcap.com"]

    def __init__(self, to_page=81, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.to_page = int(to_page)
        except (TypeError, ValueError):
            raise ValueError("to_page must be an integer")

        if self.to_page < 1:
            raise ValueError("to_page must be greater than 0")

        self.start_urls = [
            f"https://coinmarketcap.com/?page={x}"
            for x in range(1, self.to_page + 1)
        ]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("evaluate", scrolling_script),
                        PageMethod("wait_for_load_state", "networkidle"),
                    ],
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        html = await page.content()

        response = response.replace(body=html)

        for cursor in response.xpath('//table[contains(@class,"cmc-table")]//tbody[1]//tr'):
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

                "web_path": cursor.xpath('.//a/@href').get(),
            }

        await page.close()
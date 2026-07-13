import scrapy


class ConvertSpider(scrapy.Spider):
    name = "converter"
    allowed_domains = ["coinmarketcap.com"]

    OPTION_SELECTOR = (
        'xpath=//div[contains(@class,"cmc-body-wrapper")]'
        '//div[contains(@class,"cmc-select__group")]'
        '//div[contains(@class,"cmc-select__option")]'
    )

    FROM_INPUT = 'xpath=//*[@id="react-select-cmc-select__from-input"]'
    TO_INPUT = 'xpath=//*[@id="react-select-cmc-select__to-input"]'

    def __init__(self, from_coin=None, to_coin=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not from_coin:
            raise ValueError("from_coin is required")

        if not to_coin:
            raise ValueError("to_coin is required")

        if not isinstance(from_coin, str) or from_coin.isdigit():
            raise ValueError("from_coin must be a valid coin symbol")

        if not isinstance(to_coin, str) or to_coin.isdigit():
            raise ValueError("to_coin must be a valid coin symbol")

        self.from_coin = from_coin.lower()
        self.to_coin = to_coin.lower()

        self.start_urls = [
            "https://coinmarketcap.com/converter/"
        ]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_goto_kwargs": {
                        "wait_until": "networkidle",
                    },
                },
                callback=self.parse,
            )

    async def select_coin(self, page, input_selector, coin):
        inp = page.locator(input_selector)
        await inp.wait_for()
        await inp.fill(coin)

        options = page.locator(self.OPTION_SELECTOR)

        count = await options.count()

        if count == 0:
            raise ValueError(f'Unknown coin "{coin}"')

        option = options.nth(0)

        await option.wait_for()
        await option.click()

    async def parse(self, response):
        page = response.meta["playwright_page"]

        try:
            amount = page.locator(
                'xpath=//div[contains(@class,"cmc-body-wrapper")]//input[@type="number"]'
            )

            await amount.wait_for()
            await amount.fill("1")

            await self.select_coin(
                page,
                self.FROM_INPUT,
                self.from_coin,
            )

            await self.select_coin(
                page,
                self.TO_INPUT,
                self.to_coin,
            )

            await page.locator(
                'xpath=//em[contains(@class,"cmc-converter__conversion-result")]'
            ).nth(0).wait_for()

            html = await page.content()

            response = response.replace(body=html)

            from_coin_res = " ".join(
                t.strip()
                for t in response.xpath(
                    '//div[contains(@class,"cmc-converter")]'
                    '//div[contains(@class,"converter__text-row")]'
                    '//div/text()'
                ).getall()[:2]
                if t.strip()
            )

            yield {
                "FromCoin": from_coin_res,
                "ToCoin": (
                    (response.xpath(
                        '//em[contains(@class,"cmc-converter__conversion-result")]/text()'
                    ).get() or "")
                    +
                    (response.xpath(
                        '//div[contains(@class,"cmc-converter")]'
                        '//div[contains(@class,"converter__text-row")]'
                        '//div[3]/text()'
                    ).get() or "")
                ),
            }

        finally:
            await page.close()
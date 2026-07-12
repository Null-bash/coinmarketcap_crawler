from scrape.core.runner import ScraperRunner

from scrape.scrape.spiders.SymbolSearch import SymbolSearchSpider
from scrape.scrape.spiders.top_price import TopPriceSpider
from scrape.scrape.spiders.top_profit import TopProfitSpider
from scrape.scrape.spiders.converter import ConvertSpider

from simple_term_menu import TerminalMenu

import time


banner = r"""
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝

        CoinMarketCap Terminal Utility
---------------------------------------------------
"""


options = [
    "Search Cryptocurrency",
    "Highest Prices",
    "Highest Price Change",
    "Currency Exchange",
    "Exit",
]


def search_for_coin(runner: ScraperRunner):
    symbol = input("Coin symbol: ")
    try:
        job = runner.submit(
            SymbolSearchSpider,
            symbol=symbol
        )
        res = job.result()
    except Exception as e:
        print(e)
    else:
        print(res)

def top_10_by_price(runner: ScraperRunner):
    try:
        job = runner.submit(TopPriceSpider)
        res = job.result()
    except Exception as e:
        print(e)
    else:
        print(res)

def top_10_by_price_change(runner: ScraperRunner):
    tdomain = input("Time range (1h/24h/7d): ")
    try:
        job = runner.submit(
            TopProfitSpider,
            tdomain=tdomain,
        )
        res = job.result()
    except Exception as e:
        print(e)
    else:
        print(res)

def converter(runner: ScraperRunner):
    from_coin = input("From Crypto: ")
    to_coin = input("To Crypto: ")
    try:
        job = runner.submit(
            ConvertSpider,
            from_coin=from_coin,
            to_coin=to_coin,
        )
        res = job.result()
    except Exception as e:
        print(e)
    else:
        print(res)

def menu(options, runner: ScraperRunner):
    while True:
        choice = TerminalMenu(options, title="Select your operation:").show()

        if choice == 0:
            search_for_coin(runner)
        elif choice == 1:
            top_10_by_price(runner)
        elif choice == 2:
            top_10_by_price_change(runner)
        elif choice == 3:
            converter(runner)
        else:
            break

        # TerminalMenu(["Press Enter..."]).show()
        input("Press Enter...")

def show_banner(banner: str):
    for char in banner:
        print(char, end='', flush=True)
        if char.isalpha():
            time.sleep(0.05)

def main():
    global banner
    global options

    runner = ScraperRunner()

    show_banner(banner)
    menu(options, runner)
    runner.shutdown

if __name__ == "__main__":
    main()
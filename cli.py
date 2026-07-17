
import time

from scrape.core.job_executor import execute_job
from scrape.core.runner import ScraperRunner
from scrape.scrape.spiders.symbol_search import SymbolSearchSpider
from scrape.scrape.spiders.top_price import TopPriceSpider
from scrape.scrape.spiders.top_profit import TopProfitSpider
from scrape.scrape.spiders.converter import ConvertSpider
from simple_term_menu import TerminalMenu


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
    "Highest Prices(1-100)",
    "Highest Price Change(1-100)",
    "Currency Convert",
    "Exit",
]


def search_for_coin(runner: ScraperRunner):
    symbol = input("Crypto symbol: ")
    try:
		res = execute_job(
            runner,
            SymbolSearchSpider,
            symbol=symbol,
        )
    except Exception as e:
        print(e)
    else:
        print(res)

def top_by_price(runner: ScraperRunner):
    while True:
        try:
            number_of_coins = int(
                input("How many coins do you want (1-100): ")
            )

            if 1 <= number_of_coins <= 100:
                break

            print("Number must be between 1 and 100.")

        except ValueError:
            print("Please enter a valid number.")

    try:
		res = execute_job(
            runner,
            TopPriceSpider,
            number_of_coins=number_of_coins,
        )
    except Exception as e:
        print(e)

    else:
        print(res)

def top_by_price_change(runner: ScraperRunner):
    tdomain = input("Time range (1h/24h/7d): ")

    while True:
        try:
            number_of_coins = int(
                input("How many coins do you want (1-100): ")
            )

            if 1 <= number_of_coins <= 100:
                break

            print("Number must be between 1 and 100.")

        except ValueError:
            print("Please enter a valid number.")

    try:
		res = execute_job(
            runner,
            TopProfitSpider,
            tdomain=tdomain,
            number_of_coins=number_of_coins,
        )
    except Exception as e:
        print(e)

    else:
        print(res)

def converter(runner: ScraperRunner):
    from_coin = input("From Crypto: ")
    to_coin = input("To Crypto: ")
    try:
        res = execute_job(
            runner,
            ConvertSpider,
            from_coin=from_coin,
            to_coin=to_coin,
        )
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
            top_by_price(runner)
        elif choice == 2:
            top_by_price_change(runner)
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

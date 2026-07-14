from pathlib import Path
import csv


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "all_crypto.csv"


def get_url_by_sym(sym: str) -> str:
    """
    Find and return the CoinMarketCap URL path for a coin symbol.
    """
    with DATA_FILE.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            if row[1] == sym:
                return row[2]

    return None


def get_all_coins_sym() -> list[str]:
    """
    Return a list of all cryptocurrency symbols stored in the CSV file.
    """
    syms = []

    with DATA_FILE.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for row in reader:
            syms.append(row[1])

    return syms


if __name__ == "__main__":
    print(get_url_by_sym("BTC"))
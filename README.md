# CoinMarketCap crawler W/scrapy

## Installation

Clone the repository:

```bash
git clone https://github.com/Null-bash/coinmarketcap_crawler.git
cd coinmarketcap_crawler
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Install a Playwright browser:

```bash
playwright install <browser>
```

Available browser names include:

* `chromium`
* `firefox`
* `webkit`

> **Note:** If you are in Iran, this command may fail because Playwright downloads are blocked. Use a VPN or proxy before running the command.

## Environment Variables

Copy the example environment file:

Linux/macOS:

```bash
cp .env.example .env
```

Windows:

```cmd
copy .env.example .env
```

Edit the `.env` file as needed:

```env
PLAYWRIGHT_BROWSER_TYPE=chromium
PLAYWRIGHT_BROWSER_PATH=

HEADLESS=True
```

### `PLAYWRIGHT_BROWSER_TYPE`

Specifies which **Playwright bundled browser** to use.

Example:

```env
PLAYWRIGHT_BROWSER_TYPE=firefox
```

This option is used when the browser has been installed with:

```bash
playwright install firefox
```

Supported values:

* `chromium`
* `firefox`
* `webkit`

### `PLAYWRIGHT_BROWSER_PATH`

Optional.

If you want to use a browser already installed on your system instead of the Playwright bundled browser, specify its executable path.

Examples:

**Linux**

```env
PLAYWRIGHT_BROWSER_PATH=/usr/bin/google-chrome
```

**macOS**

```env
PLAYWRIGHT_BROWSER_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

**Windows**

```env
PLAYWRIGHT_BROWSER_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

When this variable is set, it takes precedence over `PLAYWRIGHT_BROWSER_TYPE`.

### `HEADLESS`

Controls whether the browser runs with or without a visible window.

```env
HEADLESS=True
```

* `True` — Run the browser in headless mode (recommended for production).
* `False` — Open the browser window (recommended for debugging).

## Running the Project

Run the CLI interface:

```bash
python cli.py
```


## Scrapy Spiders

### `all_symbols`

Extracting all coins infos like price and link.

> This spider is not available through the CLI interface.

### `SymbolSearching
Searches for a coin using its symbol.

It reads the corresponding `url_path` from `data/all_crypto.csv` and then extracts the coin's information from CoinMarketCap.

### `top_price`

Returns the 10 coins with the highest prices.

### `top_profit`

Returns the 10 coins with the highest positive percentage change.

### `exchange`

Converts one cryptocurrency to another.
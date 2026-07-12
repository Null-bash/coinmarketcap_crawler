# 🚀 CoinMarketCap Crawler

A modern **CoinMarketCap** crawler built with **Scrapy** and **Playwright** for scraping cryptocurrency data from dynamic pages.

---

## ✨ Features

- 🪙 Search cryptocurrencies by symbol
- 💵 Get the Top 10 highest-priced cryptocurrencies
- 📈 Find the Top 10 biggest gainers
- 🔄 Convert one cryptocurrency to another
- 📋 Extract all listed cryptocurrencies and their metadata
- ⚡ Fast asynchronous crawling powered by Scrapy + Playwright

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Null-bash/coinmarketcap_crawler.git
cd coinmarketcap_crawler
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```cmd
venv\Scripts\activate
```

## 3. Install the dependencies

```bash
pip install -r requirements.txt
```

## 4. Install a Playwright browser

```bash
playwright install <browser>
```

Available browsers:

- `chromium` *(recommended)*
- `firefox`
- `webkit`

> **Note**
>
> If you're located in **Iran**, Playwright downloads may be blocked. Use a **VPN** or configure a **proxy** before running the command.

---

# ⚙️ Configuration

Copy the example environment file.

### Linux / macOS

```bash
cp .env.example .env
```

### Windows

```cmd
copy .env.example .env
```

Example:

```env
PLAYWRIGHT_BROWSER_TYPE="chromium"
PLAYWRIGHT_BROWSER_PATH=

HEADLESS=True
```

---

## `PLAYWRIGHT_BROWSER_TYPE`

Selects which Playwright browser to launch.

```env
PLAYWRIGHT_BROWSER_TYPE=chromium
```

Install the corresponding browser first:

```bash
playwright install chromium
```

Supported values:

- `chromium`
- `firefox`
- `webkit`

---

## `PLAYWRIGHT_BROWSER_PATH`

**Optional**

Use an existing browser installation instead of the Playwright-managed browser.
and if you do not know how you can get your path, you can simply enter this in the shell :

```bash
which google-chrome
```

### Linux

```env
PLAYWRIGHT_BROWSER_PATH=/usr/bin/google-chrome
```

### macOS

```env
PLAYWRIGHT_BROWSER_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

### Windows

```env
PLAYWRIGHT_BROWSER_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

When this variable is set, it overrides `PLAYWRIGHT_BROWSER_TYPE`.

---

## `HEADLESS`

Controls whether Playwright launches the browser with or without a GUI.

```env
HEADLESS=True
```

| Value | Description |
|:------|:------------|
| `True` | Runs the browser in headless mode *(recommended)* |
| `False` | Opens the browser window *(useful for debugging)* |

---

# ▶️ Running the Project

After installing all dependencies and completing the setup, start the interactive CLI application with:

```bash
python cli.py
```

The CLI provides a simple interface for selecting and running the available spiders without needing to execute Scrapy commands manually.

---

# 🕷 Available Spiders

The project includes several specialized spiders for collecting cryptocurrency data from CoinMarketCap.

## `all_cryptos`

Collects metadata for **every cryptocurrency listed on CoinMarketCap**.

Extracted information includes:

* 🪙 Cryptocurrency name
* 🔖 Trading symbol
* 🔗 CoinMarketCap URL
* 📂 URL path (used internally by other spiders)

The collected data is stored in:

```text
data/all_crypto.csv
```

> **Note**
>
> This spider is designed for internal use only. It creates the local database used by other spiders and is **not exposed through the CLI**.

---

## `Symbol_search`

Searches for a cryptocurrency using its trading symbol.

### How it works

1. Reads `data/all_crypto.csv`.
2. Finds the matching cryptocurrency by symbol.
3. Retrieves its CoinMarketCap URL.
4. Visits the corresponding page using Playwright.
5. Extracts the latest market information.

Typical information includes:

* Current price
* Market capitalization
* 24-hour trading volume
* Circulating supply
* Percentage changes
* Other publicly available statistics

This spider allows users to quickly retrieve detailed information about a specific cryptocurrency without manually browsing CoinMarketCap.

---

## `top_price`

Retrieves the **10 highest-priced cryptocurrencies** currently listed on CoinMarketCap.

Useful for:

* Comparing premium-priced digital assets
* Monitoring market leaders by unit price
* Quick market overviews

---

## `top_profit`

Retrieves the **10 cryptocurrencies with the highest positive percentage gain** over the selected time period.

This spider is useful for:

* Identifying trending coins
* Monitoring top-performing assets
* Discovering strong market momentum

---

## `converter`

Converts one cryptocurrency into another using CoinMarketCap's live conversion calculator.

Example conversions include:

* BTC → ETH
* ETH → SOL
* DOGE → USDT

The spider retrieves the latest available conversion rate directly from CoinMarketCap to provide accurate results.

---

# 🛠 Tech Stack

This project is built using modern Python web-scraping technologies.

| Technology            | Purpose                                   |
| --------------------- | ----------------------------------------- |
| **Python**            | Core programming language                 |
| **Scrapy**            | Crawling framework and spider management  |
| **Playwright**        | Browser automation for dynamic content    |
| **scrapy-playwright** | Integration between Scrapy and Playwright |
| **CSV**               | Local storage for cryptocurrency metadata |

---

# 📁 Project Workflow

The recommended workflow is:

1. Run `all_cryptos` to generate or update the local cryptocurrency database.
    you cab run this part with :
    ```bash
    python all_cryptos.py
    ```
2. Launch the CLI.
3. Choose one of the available spiders.
4. View the extracted cryptocurrency data directly from the terminal.

Because the symbol database is stored locally, subsequent searches are significantly faster and require fewer requests.

---

# 📄 License

This project is intended for **educational**, **learning**, and **personal** use.

All cryptocurrency data belongs to CoinMarketCap. When using this project, please respect CoinMarketCap's Terms of Service, robots.txt policies, and applicable laws regarding automated data collection.

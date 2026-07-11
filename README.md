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
PLAYWRIGHT_BROWSER_TYPE=chromium
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

Start the CLI application:

```bash
python cli.py
```

---

# 🕷 Available Spiders

## `all_symbols`

Extracts information for all cryptocurrencies, including:

- Name
- Symbol
- CoinMarketCap URL

> **Note:** This spider is intended for internal use and is **not available** through the CLI.

---

## `SymbolSearching`

Searches for a cryptocurrency by its symbol.

The spider looks up the corresponding `url_path` inside `data/all_crypto.csv`, visits the CoinMarketCap page, and extracts the latest information.

---

## `top_price`

Returns the **10 highest-priced cryptocurrencies**.

---

## `top_profit`

Returns the **10 cryptocurrencies with the highest positive percentage change**.

---

## `converter`

Converts one cryptocurrency into another using CoinMarketCap's converter.

---

# 🛠 Tech Stack

- Python
- Scrapy
- Playwright
- scrapy-playwright

---

## 📄 License

This project is intended for educational and personal use. Please respect CoinMarketCap's Terms of Service when scraping their website.
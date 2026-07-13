# Scrapy settings for scrape project

BOT_NAME = "scrape"

SPIDER_MODULES = ["scrape.scrape.spiders"]
NEWSPIDER_MODULE = "scrape.scrape.spiders"

ADDONS = {}

# User Agent (used by UARotatorMiddleware)
USER_AGENTS = [
    "my-cool-project (http://example.com)",
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Cookies
COOKIES_ENABLED = False


# Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    "scrape.scrape.middlewares.ScrapeDownloaderMiddleware": 543,
    "scrape.scrape.middlewares.UARotatorMiddleware": 400,
}

# Feed Export
FEED_EXPORT_ENCODING = "utf-8"

# -------------------------
# Playwright Configuration
# -------------------------

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
    "executable_path": "/usr/bin/google-chrome",
}
# PLAYWRIGHT_BROWSER_TYPE = "firefox"

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000

# Logging
LOG_LEVEL = "DEBUG"
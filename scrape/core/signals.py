from scrapy import signals


def connect(crawler, collector):
    """
    Connect crawler events to the result collector handlers.
    """

    crawler.signals.connect(
        collector.item_scraped,
        signal=signals.item_scraped,
        weak=False,
    )

    crawler.signals.connect(
        collector.spider_error,
        signal=signals.spider_error,
        weak=False,
    )

    def closed(spider, reason):
        """
        Update the job state when the spider finishes.
        """
        job = collector.job

        if job.reason is None:
            job.reason = reason

        job.crawler = None

        if not job.done():
            job._done.set()

    crawler.signals.connect(
        closed,
        signal=signals.spider_closed,
        weak=False,
    )
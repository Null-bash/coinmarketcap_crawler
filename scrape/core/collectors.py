from twisted.internet import reactor


class ListCollector:
    """
    Collect scraped items in memory and handle spider errors.
    """

    def __init__(self, job):
        """
        Store the job instance used for saving results and errors.
        """
        self.job = job

    def item_scraped(self, item, response, spider):
        """
        Save each scraped item into the job results list.
        """
        self.job.results.append(
            dict(item)
        )

    def spider_error(self, failure, response, spider):
        """
        Store the first spider error and stop the crawler safely.
        """
        if self.job.exception is None:
            self.job.exception = failure.value

        reactor.callFromThread(
            spider.crawler.engine.close_spider,
            spider,
            reason="error",
        )
from threading import Event

from twisted.internet import reactor


class CrawlJob:
    """
    Manage the state and results of a running crawler job.
    """

    def __init__(self):
        """
        Initialize job status, results storage, and completion tracking.
        """
        self._done = Event()

        self.results = []
        self.exception = None
        self.reason = None

        self.crawler = None

    def wait(self, timeout=None):
        """
        Wait until the crawler finishes or the timeout expires.
        """
        return self._done.wait(timeout)

    def done(self):
        """
        Check whether the crawler job has finished.
        """
        return self._done.is_set()

    def successful(self):
        """
        Check whether the crawler completed successfully.
        """
        return (
            self.done()
            and self.exception is None
            and self.reason == "finished"
        )

    def cancelled(self):
        """
        Check whether the crawler was cancelled.
        """
        return self.reason == "cancelled"

    def cancel(self):
        """
        Cancel the running crawler if it is still active.
        """
        if self.done() or self.crawler is None:
            return False

        reactor.callFromThread(
            self.crawler.engine.close_spider,
            self.crawler.spider,
            reason="cancelled",
        )

        return True

    def result(self, timeout=None):
        """
        Return crawler results after completion.

        Raises:
            TimeoutError: If the crawler does not finish in time.
            Exception: If the crawler failed.
        """
        if not self.wait(timeout):
            raise TimeoutError("Crawler did not finish.")

        if self.exception is not None:
            raise self.exception

        return self.results
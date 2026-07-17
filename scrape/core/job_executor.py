from typing import Any, Type

from scrape.core.runner import ScraperRunner


def execute_job(runner: ScraperRunner, spider_cls: Type[Any], **spider_kwargs: Any) -> Any:
    job = runner.submit(spider_cls, **spider_kwargs)
    return job.result()

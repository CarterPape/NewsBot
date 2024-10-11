# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# type: ignore
# pylint: disable=useless-parent-delegation
# pylint: disable=abstract-class-instantiated

import pytest

from newsbot.tasking.crawl_schedulers import crawl_scheduler


def test_crawl_scheduler_not_implemented():
    class TestCrawlScheduler(crawl_scheduler.CrawlScheduler):
        def calculate_pause_time_in_seconds(self) -> float:
            return super().calculate_pause_time_in_seconds()
    
    with pytest.raises(
        NotImplementedError,
        match=(
            "TestCrawlScheduler.calculate_pause_time_in_seconds is not defined"
        ),
    ):
        TestCrawlScheduler().calculate_pause_time_in_seconds()

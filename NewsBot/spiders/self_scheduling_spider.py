# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.spiders
import NewsBot.items.dispatch
import typing_extensions
import newsbot_tasking.crawl_schedulers.uniformly_random_scheduler
import NewsBot.settings
import NewsBot.logger
import datetime
import dotenv
import os


class SelfSchedulingSpider(
    scrapy.spiders.Spider,
    NewsBot.logger.Logger,
):
    _DEBUG_SCHEDULER = (
        newsbot_tasking.crawl_schedulers.uniformly_random_scheduler.UniformlyRandomScheduler(
            minimum_interval = datetime.timedelta(seconds = 5),
            maximum_interval = datetime.timedelta(seconds = 10),
        )
    )
    
    def __init__(self):
        dotenv.load_dotenv(dotenv.find_dotenv())
        if os.getenv("ENVIRONMENT") == "development":
            self._crawl_scheduler = self._DEBUG_SCHEDULER
    
    @property
    def scheduler(self) -> newsbot_tasking.crawl_schedulers.crawl_scheduler.CrawlScheduler:
        return self._crawl_scheduler

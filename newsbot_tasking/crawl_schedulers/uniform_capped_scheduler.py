# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import NewsBot.settings
import newsbot_tasking.crawl_schedulers.crawl_scheduler
import random


class UniformCappedScheduler(newsbot_tasking.crawl_schedulers.crawl_scheduler.CrawlScheduler):
    _DEFAULT_MAXIMUM_INTERVAL =     NewsBot.settings._DEFAULT_MAXIMUM_INTERVAL
    _UNIFORM_RELATIVE_DEVIATION =   0.1
    
    def __init__(self, *,
        maximum_interval: datetime.timedelta = None,
        minimum_interval: datetime.timedelta = None,
    ):
        self._maximum_interval = (
            UniformCappedScheduler._DEFAULT_MAXIMUM_INTERVAL
            if maximum_interval is None else
            maximum_interval
        )
        self._minimum_interval = (
            self._maximum_interval * (
                1.0 - UniformCappedScheduler._UNIFORM_RELATIVE_DEVIATION
            )
        )
    
    def get_pause_time_in_seconds(self):
        return (
            random.uniform(
                self._minimum_interval,
                self._maximum_interval,
            ).total_seconds()
        )

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import newsbot_tasking.crawl_schedulers.crawl_scheduler
import random


class UniformlyRandomScheduler(newsbot_tasking.crawl_schedulers.crawl_scheduler.CrawlScheduler):
    _UNIFORM_RELATIVE_DEVIATION =   0.1
    
    def __init__(self, *,
        minimum_interval: datetime.timedelta,
        maximum_interval: datetime.timedelta,
    ):
        self._minimum_interval = minimum_interval
        self._maximum_interval = maximum_interval
    
    @property
    def pause_time_in_seconds(self):
        return (
            random.uniform(
                self._minimum_interval,
                self._maximum_interval,
            ).total_seconds()
        )

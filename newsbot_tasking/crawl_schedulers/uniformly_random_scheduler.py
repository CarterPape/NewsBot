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
    def __init__(self, *,
        minimum_interval: datetime.timedelta,
        maximum_interval: datetime.timedelta,
        first_call_is_immediate = False,
    ):
        self._minimum_interval = minimum_interval
        self._maximum_interval = maximum_interval
        
        self._next_call_is_immediate = first_call_is_immediate
    
    @property
    def pause_time_in_seconds(self):
        if self._next_call_is_immediate:
            self._next_call_is_immediate = False
            return 0
        
        return (
            random.uniform(
                self._minimum_interval,
                self._maximum_interval,
            ).total_seconds()
        )

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import datetime
import random

from newsbot.tasking.crawl_schedulers import crawl_scheduler


class UniformlyRandomScheduler(crawl_scheduler.CrawlScheduler):
    def __init__(self, *,
        minimum_interval: datetime.timedelta,
        maximum_interval: datetime.timedelta,
        first_call_is_immediate = False,
    ):
        assert minimum_interval <= maximum_interval, \
            "minimum_interval must be less than or equal to maximum_interval"
        self._minimum_interval = minimum_interval
        self._maximum_interval = maximum_interval
        
        self._next_call_is_immediate = first_call_is_immediate
    
    def calculate_pause_time_in_seconds(self):
        if self._next_call_is_immediate:
            self._next_call_is_immediate = False
            return 0
        
        return (
            random.uniform(
                self._minimum_interval.total_seconds(),
                self._maximum_interval.total_seconds(),
            )
        )

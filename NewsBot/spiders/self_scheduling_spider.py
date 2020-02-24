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
            first_call_is_immediate =   True,
        )
    )
    
    @classmethod
    def make_a_scheduler(klass, *, suggested_scheduler = None):
        if os.getenv("ENVIRONMENT") == "development" or suggested_scheduler == None:
            new_scheduler = klass._DEBUG_SCHEDULER
        else:
            new_scheduler = suggested_scheduler
        
        return new_scheduler

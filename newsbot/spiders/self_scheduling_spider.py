# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import scrapy.spiders
import scrapy.crawler
import newsbot.tasking.crawl_schedulers.uniformly_random_scheduler as uniformly_random_scheduler
import datetime
import dotenv
import os
import copy
import abc


class SelfSchedulingSpider(
    scrapy.spiders.Spider,
    metaclass = abc.ABCMeta,
):
    _DEBUG_SCHEDULER = (
        uniformly_random_scheduler.UniformlyRandomScheduler(
            minimum_interval = datetime.timedelta(seconds = 5),
            maximum_interval = datetime.timedelta(seconds = 10),
            first_call_is_immediate =   True,
        )
    )
    
    @classmethod
    def make_a_scheduler(klass, *,
        from_crawler: scrapy.crawler.Crawler,
        suggested_scheduler = None
    ):
        if (
            from_crawler.settings.get("_ENVIRONMENT") == "development"
        ) or (
            suggested_scheduler == None
        ):
            new_scheduler = copy.copy(klass._DEBUG_SCHEDULER)
        else:
            new_scheduler = suggested_scheduler
        
        logging.debug(f"Using scheduler {new_scheduler} for a spider of class {klass}")
        
        return new_scheduler

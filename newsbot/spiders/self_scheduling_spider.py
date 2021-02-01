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
    @classmethod
    def make_a_scheduler(klass, *,
        from_crawler: scrapy.crawler.Crawler,
        suggested_scheduler = None
    ):
        if from_crawler.settings.get("_FORCE_SCHEDULER") != None:
            new_scheduler = copy.copy(
                from_crawler.settings.get("_FORCE_SCHEDULER")
            )
        else:
            new_scheduler = suggested_scheduler
        
        logging.debug(f"Using scheduler {new_scheduler} for a spider of class {klass}")
        
        return new_scheduler

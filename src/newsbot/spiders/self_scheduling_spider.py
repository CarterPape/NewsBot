# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import copy
import abc
import logging
import typing
import scrapy.spiders
import scrapy.crawler
import scrapy.http

from newsbot.tasking.crawl_schedulers import crawl_scheduler


class SelfSchedulingSpider(
    scrapy.spiders.Spider,
    metaclass = abc.ABCMeta,
):
    @classmethod
    def make_a_scheduler(klass, *,
        from_crawler: scrapy.crawler.Crawler,
        suggested_scheduler: crawl_scheduler.CrawlScheduler | None = None
    ) -> crawl_scheduler.CrawlScheduler:
        if from_crawler.settings.get("_FORCE_SCHEDULER") is not None:
            new_scheduler = copy.copy(
                from_crawler.settings.get("_FORCE_SCHEDULER")
            )
        else:
            new_scheduler = suggested_scheduler
        
        logging.debug(f"Using scheduler {new_scheduler} for a spider of class {klass}")
        
        return typing.cast(crawl_scheduler.CrawlScheduler, new_scheduler)
    
    def parse(self,
        response: scrapy.http.Response,
        **kwargs: typing.Any
    ) -> typing.Any:
        return super().parse(response, **kwargs)

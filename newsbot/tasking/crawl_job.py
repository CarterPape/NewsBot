# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.crawler
import typing
import logging
import twisted.internet.defer
import twisted.internet.reactor
import random
import newsbot.tasking.crawl_schedulers.crawl_scheduler as crawl_scheduler
import newsbot.spiders.self_scheduling_spider as self_scheduling_spider


class CrawlJob:
    def __init__(self, *,
        from_runner:        scrapy.crawler.CrawlerRunner,
        spider_class:       type,
    ):
        assert(issubclass(spider_class, self_scheduling_spider.SelfSchedulingSpider))
        self._runner =          from_runner
        self._crawler =         scrapy.crawler.Crawler(
            spider_class,
            settings =  self._runner.settings,
        )
        self._scheduler: crawl_scheduler.CrawlScheduler = (
            spider_class.make_a_scheduler(from_crawler = self._crawler)
        )
    
    def crawl_then_repeat_later(self):
        logging.info(f"Starting a crawl with a spider of class {self._crawler.spidercls}")
        
        deferred = self._runner.crawl(self._crawler)
        deferred.addCallback(self.schedule_a_crawl)
    
    def schedule_a_crawl(self, deferred_result = None):
        pause_time = self._scheduler.pause_time_in_seconds
        
        logging.info(f"Scheduling a crawl with a spider of class {self._crawler.spidercls} for {pause_time} seconds from now")
        
        twisted.internet.reactor.callLater(
            pause_time,
            self.crawl_then_repeat_later,
        )

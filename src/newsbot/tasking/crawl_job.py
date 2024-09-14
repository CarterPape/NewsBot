# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging

import scrapy.crawler
import twisted.internet.defer
import twisted.internet.reactor

from newsbot.tasking.crawl_schedulers import crawl_scheduler
from newsbot.spiders import self_scheduling_spider


class CrawlJob:
    def __init__(self, *,
        from_runner:        scrapy.crawler.CrawlerRunner,
        spider_class:       type,
    ):
        assert issubclass(spider_class, self_scheduling_spider.SelfSchedulingSpider)
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
    
    def schedule_a_crawl(self, _ = None):
        pause_time = self._scheduler.pause_time_in_seconds
        
        logging.info(
            f"Scheduling a crawl with a spider of class {self._crawler.spidercls} "
            f"for {pause_time} seconds from now"
        )
        
        twisted.internet.reactor.callLater( # type: ignore # pylint: disable=no-member
            pause_time,
            self.crawl_then_repeat_later,
        )

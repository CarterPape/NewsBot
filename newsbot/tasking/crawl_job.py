# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.crawler
import datetime
import typing
import twisted.internet.defer
import twisted.internet.reactor
import random
import newsbot.tasking.crawl_schedulers.crawl_scheduler as crawl_scheduler
import newsbot.spiders.self_scheduling_spider as self_scheduling_spider
import newsbot.logger as logger


class CrawlJob(logger.Logger):
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
        self._scheduler: crawl_scheduler.CrawlScheduler = spider_class.make_a_scheduler()
    
    def crawl_then_repeat_later(self):
        deferred = self._runner.crawl(self._crawler)
        deferred.addBoth(self.schedule_a_crawl)
    
    def schedule_a_crawl(self, deferred_result = None):
        twisted.internet.reactor.callLater(
            self._scheduler.pause_time_in_seconds,
            self.crawl_then_repeat_later,
        )

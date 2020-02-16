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
import newsbot_tasking.crawl_schedulers.crawl_scheduler


class CrawlJob(object):    
    def __init__(self, *,
        from_runner:        scrapy.crawler.CrawlerRunner,
        spider_class:       type,
    ):
        self._runner =          from_runner
        self._crawler =         scrapy.crawler.Crawler(
            spider_class,
            settings =  self._runner.settings,
        )
    
    def schedule_crawling(self):
        deferred = self._runner.crawl(self._crawler)
        deferred.addCallback(
            self._schedule_again,
            self._crawler.spider.scheduler
        )
    
    def _schedule_again(
        self,
        result,
        scheduler: newsbot_tasking.crawl_schedulers.crawl_scheduler.CrawlScheduler,
    ):
        twisted.internet.reactor.callLater(
            scheduler.pause_time_in_seconds,
            self.schedule_crawling,
        )

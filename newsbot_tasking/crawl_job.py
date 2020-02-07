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


class CrawlJob(object):
    _UNIFORM_RELATIVE_DEVIATION = 0.10
    
    def __init__(self, *,
        from_runner:        scrapy.crawler.CrawlerRunner,
        spider_class:       type,
    ):
        self._runner =          from_runner
        self._spider_class =    spider_class
        self._crawl_scheduler = spider_class.get_scheduler()
    
    def schedule_crawling(self):
        deferred = self._runner.crawl(self._spider_class)
        deferred.addCallback(self._schedule_again)
    
    def _schedule_again(self, result):
        twisted.internet.reactor.callLater(
            self._crawl_scheduler.get_pause_time_in_seconds(),
            self.schedule_crawling,
        )

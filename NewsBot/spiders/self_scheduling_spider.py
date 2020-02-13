# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.http
import NewsBot.items.dispatch
import typing_extensions
import newsbot_tasking.crawl_schedulers as NewsBotCrawlSchedulers


class SelfScheduling(typing_extensions.Protocol):
    @staticmethod
    def get_scheduler() -> NewsBotCrawlSchedulers.CrawlScheduler:
        raise NotImplementedError

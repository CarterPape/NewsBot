# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing

import scrapy.crawler
import scrapy.utils.project

from newsbot.tasking import crawl_job


class NewsBotJobRegistry:
    def __init__(self, *,
        from_spider_classes: typing.List[type],
    ):
        self._runner: scrapy.crawler.CrawlerRunner = (
            scrapy.crawler.CrawlerRunner(
                settings = scrapy.utils.project.get_project_settings(),
            )
        )
        
        self._jobs: typing.List[crawl_job.CrawlJob] = [
            crawl_job.CrawlJob(
                from_runner =       self._runner,
                spider_class =      each_spider_class,
            )
            for each_spider_class in from_spider_classes
        ]
    
    def schedule_all_jobs(self):
        for job in self._jobs:
            job.schedule_a_crawl()

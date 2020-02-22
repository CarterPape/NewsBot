# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.crawler
import scrapy.utils.project
import newsbot_tasking.crawl_job
import datetime


class NewsBotJobRegistry(object):
    def __init__(self, *,
        from_spider_classes: [type],
    ):
        self._runner: scrapy.crawler.CrawlerRunner = (
            scrapy.crawler.CrawlerRunner(
                settings = scrapy.utils.project.get_project_settings(),
            )
        )
        
        self._jobs: [newsbot_tasking.crawl_job.CrawlJob] = [
            newsbot_tasking.crawl_job.CrawlJob(
                from_runner =       self._runner,
                spider_class =      each_spider_class,
            )
            for each_spider_class in from_spider_classes
        ]
    
    def schedule_all_jobs(self):
        for job in self._jobs:
            job.schedule_crawling()

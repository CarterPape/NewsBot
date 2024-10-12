# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access

import unittest
import unittest.mock

from newsbot.tasking import job_registry

class TestNewsBotJobRegistry(unittest.TestCase):
    def setUp(self):
        job_patcher = unittest.mock.patch('newsbot.tasking.crawl_job.CrawlJob')
        runner_patcher = unittest.mock.patch('scrapy.crawler.CrawlerRunner')
        
        self.mock_crawl_job = job_patcher.start()
        self.mock_crawler_runner = runner_patcher.start()
        
        self.addCleanup(job_patcher.stop)
        self.addCleanup(runner_patcher.stop)
        
        self.mock_spider_classes = [unittest.mock.create_autospec(type)]
        
        self.registry = job_registry.NewsBotJobRegistry(
            from_spider_classes=self.mock_spider_classes
        )
        
        super().setUp()
    
    def test_schedule_all_jobs(self):
        self.registry.schedule_all_jobs()
        
        # Ensure that schedule_a_crawl is called for each job
        for job in self.registry._jobs:
            job.schedule_a_crawl.assert_called_once()

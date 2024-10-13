# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access, too-many-instance-attributes

import unittest
import unittest.mock

from newsbot.tasking import crawl_job
from newsbot.tasking.crawl_schedulers import crawl_scheduler
from newsbot.spiders import self_scheduling_spider

class MockSpider(self_scheduling_spider.SelfSchedulingSpider):
    mock_scheduler = unittest.mock.create_autospec(crawl_scheduler.CrawlScheduler)
    
    @classmethod
    def make_a_scheduler(klass, **_) -> crawl_scheduler.CrawlScheduler:
        return klass.mock_scheduler

class TestCrawlJob(unittest.TestCase):
    def setUp(self):
        self.runner_instantiator_patch = unittest.mock.patch("scrapy.crawler.CrawlerRunner")
        self.crawler_instantiator_patch = unittest.mock.patch("scrapy.crawler.Crawler")
        
        self.mock_runner_instantiator = self.runner_instantiator_patch.start()
        self.mock_crawler_instantiator = self.crawler_instantiator_patch.start()
        
        self.addCleanup(self.runner_instantiator_patch.stop)
        self.addCleanup(self.crawler_instantiator_patch.stop)
        
        self.mock_runner_instance = self.mock_runner_instantiator.return_value
        self.mock_crawler_instance = self.mock_crawler_instantiator.return_value
    
    def test_init(self):
        job = crawl_job.CrawlJob(
            from_runner = self.mock_runner_instance,
            spider_class = MockSpider
        )
        
        self.mock_crawler_instantiator.assert_called_once_with(
            MockSpider,
            settings = self.mock_runner_instance.settings
        )
        
        assert job._runner == self.mock_runner_instance
        assert job._crawler == self.mock_crawler_instance
        assert job._scheduler == MockSpider.mock_scheduler
    
    @unittest.mock.patch("twisted.internet.reactor.callLater", autospec=True)
    def test_crawl_then_repeat_later(self, _):
        job = crawl_job.CrawlJob(
            from_runner=self.mock_runner_instance,
            spider_class=MockSpider
        )
        
        mock_deferred = unittest.mock.Mock()
        self.mock_runner_instance.crawl.return_value = mock_deferred
        
        job.crawl_then_repeat_later()
        
        self.mock_runner_instance.crawl.assert_called_once_with(self.mock_crawler_instance)
        mock_deferred.addCallback.assert_called_once_with(job.schedule_a_crawl)
        
    @unittest.mock.patch("twisted.internet.reactor.callLater", autospec=True)
    def test_schedule_a_crawl(self,
        mock_call_later: unittest.mock.Mock,
    ):
        job = crawl_job.CrawlJob(
            from_runner=self.mock_runner_instance,
            spider_class=MockSpider
        )
        
        pause_time = 10
        MockSpider.mock_scheduler.calculate_pause_time_in_seconds.return_value = pause_time
        
        job.schedule_a_crawl()
        
        MockSpider.mock_scheduler.calculate_pause_time_in_seconds.assert_called_once()
        mock_call_later.assert_called_once_with(pause_time, job.crawl_then_repeat_later)

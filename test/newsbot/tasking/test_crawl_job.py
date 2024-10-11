# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access, too-many-instance-attributes

import unittest
import unittest.mock

from newsbot.tasking import crawl_job
from newsbot.spiders import self_scheduling_spider

class MockSpider(self_scheduling_spider.SelfSchedulingSpider):
    pass

class TestCrawlJob(unittest.TestCase):
    def setUp(self):
        self.runner_patcher = unittest.mock.patch('scrapy.crawler.CrawlerRunner')
        self.crawler_patcher = unittest.mock.patch('scrapy.crawler.Crawler')
        self.scheduler_patcher = unittest.mock.patch(
            'newsbot.tasking.crawl_schedulers.crawl_scheduler.CrawlScheduler'
        )
        
        self.mock_runner = self.runner_patcher.start()
        self.mock_crawler = self.crawler_patcher.start()
        self.mock_scheduler = self.scheduler_patcher.start()
        
        self.addCleanup(self.runner_patcher.stop)
        self.addCleanup(self.crawler_patcher.stop)
        self.addCleanup(self.scheduler_patcher.stop)
        
        self.mock_runner_instance = self.mock_runner.return_value
        self.mock_crawler_instance = self.mock_crawler.return_value
        self.mock_scheduler_instance = self.mock_scheduler.return_value
    
    @unittest.mock.patch.object(
        self_scheduling_spider.SelfSchedulingSpider, 'make_a_scheduler', autospec=True
    )
    def test_init_creates_crawler_and_scheduler(self, mock_make_a_scheduler: unittest.mock.Mock):
        mock_make_a_scheduler.return_value = self.mock_scheduler_instance
        
        job = crawl_job.CrawlJob(
            from_runner=self.mock_runner_instance,
            spider_class=MockSpider
        )
        
        self.mock_crawler.assert_called_once_with(
            MockSpider,
            settings=self.mock_runner_instance.settings
        )
        mock_make_a_scheduler.assert_called_once_with(from_crawler=self.mock_crawler_instance)
        assert job._runner == self.mock_runner_instance
        assert job._crawler == self.mock_crawler_instance
        assert job._scheduler == self.mock_scheduler_instance
    
    @unittest.mock.patch('twisted.internet.reactor.callLater', autospec=True)
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
        
    @unittest.mock.patch('twisted.internet.reactor.callLater', autospec=True)
    @unittest.mock.patch.object(
        MockSpider, 'make_a_scheduler', autospec=True
    )
    def test_schedule_a_crawl(self,
        mock_make_a_scheduler: unittest.mock.Mock,
        mock_call_later: unittest.mock.Mock,
    ):
        mock_make_a_scheduler.return_value = self.mock_scheduler_instance
        
        job = crawl_job.CrawlJob(
            from_runner=self.mock_runner_instance,
            spider_class=MockSpider
        )
        
        pause_time = 10
        self.mock_scheduler_instance.calculate_pause_time_in_seconds.return_value = pause_time
        
        job.schedule_a_crawl()
        
        self.mock_scheduler_instance.calculate_pause_time_in_seconds.assert_called_once()
        mock_call_later.assert_called_once_with(pause_time, job.crawl_then_repeat_later)

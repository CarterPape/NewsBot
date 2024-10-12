# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access

import datetime
import zoneinfo
import unittest

import scrapy.http
import scrapy.crawler

from newsbot.spiders import dispatch_call_log_spider
from newsbot.tasking.crawl_schedulers import crawl_scheduler
from newsbot.tasking.crawl_schedulers import uniformly_random_scheduler


class TestDispatchCallLogSpider(unittest.TestCase):
    def setUp(self):
        self.spider = dispatch_call_log_spider.DispatchCallLogSpider()
    
    def test_start_requests(self):
        requests = self.spider.start_requests()
        assert len(requests) == 1
        assert isinstance(requests[0], scrapy.http.FormRequest)
        assert requests[0].url == "https://call-log-api.edispatches.com/calls/"
        assert \
            requests[0].body \
            == b'ddl-state=UT&ddl-county=Grand&ddl-company=ALL&ddl-limit=ALL'
        assert requests[0].callback == self.spider.parse_call_log # pylint: disable=comparison-with-callable
    
    def test_parse_call_log(self):
        html_content = """
        <html>
            <body>
                <div id="call-log-info">
                    <table>
                        <tr>
                            <td><audio src="audio1.mp3"></audio></td>
                            <td>Agency1</td>
                            <td></td>
                            <td>2023-10-01 12:00:00</td>
                        </tr>
                        <tr>
                            <td><audio src="audio2.mp3"></audio></td>
                            <td>Agency2</td>
                            <td></td>
                            <td>2023-10-01 13:00:00</td>
                        </tr>
                    </table>
                </div>
            </body>
        </html>
        """
        response = scrapy.http.HtmlResponse(
            url="https://call-log-api.edispatches.com/calls/",
            body=html_content,
            encoding='utf-8'
        )
        dispatches = self.spider.parse_call_log(response)
        
        assert len(dispatches) == 2
        assert dispatches[0]["file_URLs"] == ["audio1.mp3"]
        assert dispatches[0]["dispatched_agency"] == "Agency1"
        assert \
            dispatches[0]["datetime_dispatched"] \
            == datetime.datetime(2023, 10, 1, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Denver"))
        
        assert dispatches[1]["file_URLs"] == ["audio2.mp3"]
        assert dispatches[1]["dispatched_agency"] == "Agency2"
        assert \
            dispatches[1]["datetime_dispatched"] == \
            datetime.datetime(2023, 10, 1, 13, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Denver"))
        
    def test_make_a_scheduler_default(self):
        crawler = scrapy.crawler.Crawler(spidercls=dispatch_call_log_spider.DispatchCallLogSpider)
        scheduler = self.spider.make_a_scheduler(from_crawler=crawler)
        
        assert isinstance(scheduler, uniformly_random_scheduler.UniformlyRandomScheduler)
        assert scheduler._maximum_interval == datetime.timedelta(minutes=11)
        assert scheduler._minimum_interval == datetime.timedelta(minutes=10)

    def test_make_a_scheduler_custom(self):
        class CustomScheduler(crawl_scheduler.CrawlScheduler):
            def calculate_pause_time_in_seconds(self) -> float:
                return 0
        
        crawler = scrapy.crawler.Crawler(spidercls=dispatch_call_log_spider.DispatchCallLogSpider)
        custom_scheduler = CustomScheduler()
        scheduler = self.spider.make_a_scheduler(
            from_crawler=crawler,
            suggested_scheduler=custom_scheduler
        )
        assert scheduler is custom_scheduler

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2024 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #
# pylint: disable=protected-access

import datetime
import zoneinfo

from test.newsbot.spiders import fixture_spider_test

import pytest

import scrapy.http
import scrapy.crawler
import scrapy.utils.conf

from newsbot.spiders import dispatch_call_log_spider
from newsbot.tasking.crawl_schedulers import crawl_scheduler
from newsbot.tasking.crawl_schedulers import uniformly_random_scheduler
from newsbot.items import dispatch


class TestDispatchCallLogSpider(fixture_spider_test.SpiderTestCase):
    def setUp(self):
        self.spider: dispatch_call_log_spider.DispatchCallLogSpider = (
            dispatch_call_log_spider.DispatchCallLogSpider()
        )
        
        self.call_log_url = "https://call-log-api.edispatches.com/calls/"
        
        self.call_log_page_snapshot_path = self._page_snapshot_path(from_relative_filename=
            "test/test_data/page_snapshots/dispatch_call_log_page@2024-10-16.html",
        )
    
    def test_start_requests(self):
        requests = self.spider.start_requests()
        assert len(requests) == 1
        assert isinstance(requests[0], scrapy.http.FormRequest)
        assert requests[0].url == self.call_log_url
        assert (
            requests[0].body
            == b"ddl-state=UT&ddl-county=Grand&ddl-company=ALL&ddl-limit=ALL"
        )
        assert requests[0].callback == self.spider.parse_call_log # pylint: disable=comparison-with-callable
    
    def test_parse_call_log_from_snapshot(self):
        with open(
            self.call_log_page_snapshot_path,
            "r",
            encoding = "utf8"
        ) as file:
            html_content = file.read()
        
        response = scrapy.http.HtmlResponse(
            url = self.call_log_url,
            body = html_content,
            encoding = "utf-8",
        )
        dispatches = self.spider.parse_call_log(response)
        
        assert len(dispatches) == 2
        assert dispatches[0]["file_URLs"] == [
            "https://audio.edispatches.com/play/2024-10-16-153458-GrandCountyEMS-D11440.mp3"
        ]
        assert dispatches[0]["dispatched_agency"] == "GrandCountyEMS"
        assert (
            dispatches[0]["datetime_dispatched"]
            == datetime.datetime(
                2024, 10, 16, 15, 34, 58,
                tzinfo=zoneinfo.ZoneInfo("America/Denver")
            )
        )
        
        assert dispatches[1]["file_URLs"] == [
            "https://audio.edispatches.com/play/2024-10-15-221008-GrandCountyEMS-D11440.mp3"
        ]
        assert dispatches[1]["dispatched_agency"] == "GrandCountyEMS"
        assert (
            dispatches[1]["datetime_dispatched"]
            == datetime.datetime(
                2024, 10, 15, 22, 10, 8,
                tzinfo=zoneinfo.ZoneInfo("America/Denver")
            )
        )
    
    @pytest.mark.webtest
    def test_parse_call_log_from_cache(self):
        print("HEY")
        html_content = self._retrieve_possibly_cached_page_body(
            method = "POST",
            url = self.call_log_url,
            data = {
                "ddl-state": "UT",
                "ddl-county": "Grand",
                "ddl-company": "ALL",
                "ddl-limit": "ALL"
            }
        )
        
        response = scrapy.http.HtmlResponse(
            url = self.call_log_url,
            body = html_content,
            encoding = "utf-8",
        )
        dispatches = self.spider.parse_call_log(response)
        
        if len(dispatches) == 0:
            pytest.skip("No dispatches found in the live call log")
        else:
            for each_dispatch in dispatches:
                assert isinstance(each_dispatch, dispatch.Dispatch)
                assert isinstance(each_dispatch["file_URLs"], list)
                assert all(isinstance(each_URL, str) for each_URL in each_dispatch["file_URLs"])
                assert isinstance(each_dispatch["dispatched_agency"], str)
                assert each_dispatch["dispatched_agency"] != ""
                assert isinstance(each_dispatch["datetime_dispatched"], datetime.datetime)
    
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
        
        assert scheduler == custom_scheduler

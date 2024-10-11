# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import datetime

import zoneinfo

import scrapy
import scrapy.http
import scrapy.crawler

from newsbot.spiders import self_scheduling_spider
from newsbot.tasking.crawl_schedulers import uniformly_random_scheduler
from newsbot.items import dispatch


class DispatchCallLogSpider(self_scheduling_spider.SelfSchedulingSpider):
    name =              __name__
    allowed_domains =   ["edispatches.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "newsbot.item_pipelines.emailed_item_filter.EmailedItemFilter":     10,
            "newsbot.item_pipelines.file_downloader.FileDownloader":            400,
            "newsbot.item_pipelines.item_emailer.ItemEmailer":                  900,
            "newsbot.item_pipelines.emailed_item_recorder.EmailedItemRecorder": 990,
        }
    }
    
    def __init__(self):
        super().__init__()
        self._dispatch_log_row =                 "//*[@id='call-log-info']//table/tr"
        self._dispatch_audio_relative_xpath =    "./td[1]/audio/@src"
        self._dispatched_agency_relative_xpath = "./td[2]/text()"
        self._dispatch_time_relative_xpath =     "./td[4]/text()"
    
    @classmethod
    def make_a_scheduler(klass, *,
        from_crawler: scrapy.crawler.Crawler,
        suggested_scheduler = None
    ):
        if suggested_scheduler is None:
            new_scheduler = uniformly_random_scheduler.UniformlyRandomScheduler(
                maximum_interval =  datetime.timedelta(minutes = 11),
                minimum_interval =  datetime.timedelta(minutes = 10),
            )
        else:
            new_scheduler = suggested_scheduler
        
        return super().make_a_scheduler(
            from_crawler =          from_crawler,
            suggested_scheduler =   new_scheduler
        )
    
    def start_requests(self) -> list[scrapy.http.Request]:
        return [
            scrapy.FormRequest(
                "https://call-log-api.edispatches.com/calls/",
                formdata = {
                    "ddl-state":    "UT",
                    "ddl-county":   "Grand",
                    "ddl-company":  "ALL",
                    "ddl-limit":    "ALL",
                },
                callback = self.parse_call_log,
            )
        ]
    
    def parse_call_log(self,
        response: scrapy.http.HtmlResponse
    ) -> list[dispatch.Dispatch]:
        all_dispatch_log_rows = response.xpath(self._dispatch_log_row)
        all_dispatches = [
            dispatch.Dispatch(
                file_URLs =             one_row.xpath(self._dispatch_audio_relative_xpath).getall(),
                dispatched_agency =     one_row.xpath(self._dispatched_agency_relative_xpath).get(),
                datetime_dispatched =   datetime.datetime.strptime(
                    one_row.xpath(self._dispatch_time_relative_xpath).get() or "",
                    "%Y-%m-%d %H:%M:%S",
                ).replace(tzinfo = zoneinfo.ZoneInfo("America/Denver")),
            )
            for one_row in all_dispatch_log_rows
        ]
        
        logging.info(f"Found {len(all_dispatches)} dispatches")
        
        return all_dispatches

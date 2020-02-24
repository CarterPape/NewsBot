# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.http
import NewsBot.spiders.self_scheduling_spider
import NewsBot.items.dispatch
import newsbot_tasking.crawl_schedulers.uniformly_random_scheduler as uniformly_random_scheduler
import newsbot_tasking.crawl_schedulers.crawl_scheduler
import datetime


class DispatchCallLogSpider(NewsBot.spiders.self_scheduling_spider.SelfSchedulingSpider):
    name =              __name__
    allowed_domains =   ["edispatches.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "NewsBot.item_pipelines.emailed_item_filter.EmailedItemFilter":     10,
            "NewsBot.item_pipelines.file_downloader.FileDownloader":            400,
            "NewsBot.item_pipelines.datetime_cruncher.DatetimeCruncher":        500,
            "NewsBot.item_pipelines.item_emailer.ItemEmailer":                  900,
            "NewsBot.item_pipelines.emailed_item_recorder.EmailedItemRecorder": 990,
        }
    }
    
    def __init__(self):
        self._dispatch_log_row =                 "//*[@id='call-log-info']//table/tr"
        self._dispatch_audio_relative_xpath =    "./td[1]/audio/@src"
        self._dispatched_agency_relative_xpath = "./td[2]/text()"
        self._dispatch_time_relative_xpath =     "./td[4]/text()"
    
    @classmethod
    def make_a_scheduler(klass, *, suggested_scheduler = None):
        if suggested_scheduler == None:
            new_scheduler = uniformly_random_scheduler.UniformlyRandomScheduler(
                maximum_interval =  datetime.timedelta(minutes = 6),
                minimum_interval =  datetime.timedelta(minutes = 4),
            )
        else:
            new_scheduler = suggested_scheduler
        
        return super().make_a_scheduler(suggested_scheduler = new_scheduler)
    
    def start_requests(self) -> [scrapy.http.Request]:
        return [
            scrapy.FormRequest(
                "https://www.edispatches.com/call-log/index.php",
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
    ) -> [NewsBot.items.dispatch.Dispatch]:
        all_dispatch_log_rows = response.xpath(self._dispatch_log_row)
        all_dispatches = [
            NewsBot.items.dispatch.Dispatch(
                file_URLs =             one_row.xpath(self._dispatch_audio_relative_xpath).getall(),
                source_date_string =    one_row.xpath(self._dispatch_time_relative_xpath).get(),
                source_date_format =    "%Y-%m-%d %H:%M:%S",
                dispatched_agency =     one_row.xpath(self._dispatched_agency_relative_xpath).get(),
            )
            for one_row in all_dispatch_log_rows
        ]
        return all_dispatches

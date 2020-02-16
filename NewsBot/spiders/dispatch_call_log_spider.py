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
import newsbot_tasking.crawl_schedulers.uniformly_random_scheduler
import newsbot_tasking.crawl_schedulers.crawl_scheduler
import datetime


class DispatchCallLogSpider(NewsBot.spiders.self_scheduling_spider.SelfSchedulingSpider):
    name =              "DispatchCallLogSpider"
    allowed_domains =   ["edispatches.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "NewsBot.item_pipelines.dispatch_audio_downloader.DispatchAudioDownloader":     100,
            "NewsBot.item_pipelines.dispatch_datetime_cruncher.DispatchDatetimeCruncher":   200,
            "NewsBot.item_pipelines.item_emailer.ItemEmailer":                              500,
        }
    }
    
    def __init__(self):
        self._dispatch_log_row =                 "//*[@id='call-log-info']//table/tr"
        self._dispatch_audio_relative_xpath =    "./td[1]/audio/@src"
        self._dispatched_agency_relative_xpath = "./td[2]/text()"
        self._dispatch_time_relative_xpath =     "./td[4]/text()"
        
        self._crawl_scheduler = (
            newsbot_tasking.crawl_schedulers.uniformly_random_scheduler.UniformlyRandomScheduler(
                maximum_interval =  datetime.timedelta(minutes = 6),
                minimum_interval =  datetime.timedelta(minutes = 4),
            )
        )
        
        super().__init__()
    
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
                audio_URL =             one_row.xpath(self._dispatch_audio_relative_xpath).get(),
                dispatched_agency =     one_row.xpath(self._dispatched_agency_relative_xpath).get(),
                dispatch_date_string =  one_row.xpath(self._dispatch_time_relative_xpath).get(),
            )
            for one_row in all_dispatch_log_rows
        ]
        return all_dispatches
    
    @property
    def scheduler(self) -> newsbot_tasking.crawl_schedulers.crawl_scheduler.CrawlScheduler:
        return self._crawl_scheduler

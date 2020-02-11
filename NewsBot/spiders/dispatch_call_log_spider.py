# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.http
import NewsBot.spiders as NewsBotSpiders
import NewsBot.items.dispatch
import newsbot_tasking.crawl_schedulers


class DispatchCallLogSpider(scrapy.Spider, NewsBotSpiders.SelfScheduling):
    name =              "DispatchCallLogSpider"
    allowed_domains =   ["edispatches.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "NewsBot.item_pipelines.DispatchAudioDownloader":   100,
            "NewsBot.item_pipelines.DispatchDatetimeCruncher":  200,
            "NewsBot.item_pipelines.ItemEmailer":               500,
        }
    }
    _crawl_scheduler =   newsbot_tasking.crawl_schedulers.UniformCappedScheduler()
    
    _DISPATCH_LOG_ROW =                 "//*[@id='call-log-info']//table/tr"
    _DISPATCH_AUDIO_RELATIVE_XPATH =    "./td[1]/audio/@src"
    _DISPATCHED_AGENCY_RELATIVE_XPATH = "./td[2]/text()"
    _DISPATCH_TIME_RELATIVE_XPATH =     "./td[4]/text()"
    
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

    def parse_call_log(self, response: scrapy.http.HtmlResponse) -> [NewsBot.items.Dispatch]:
        allDispatchLogRows = response.xpath(self._DISPATCH_LOG_ROW)
        allDispatches = [
            NewsBot.items.Dispatch(
                audio_URL =             oneRow.xpath(self._DISPATCH_AUDIO_RELATIVE_XPATH).get(),
                dispatched_agency =     oneRow.xpath(self._DISPATCHED_AGENCY_RELATIVE_XPATH).get(),
                dispatch_date_string =  oneRow.xpath(self._DISPATCH_TIME_RELATIVE_XPATH).get(),
            )
            for oneRow in allDispatchLogRows
        ]
        return allDispatches
    
    @staticmethod
    def get_scheduler() -> newsbot_tasking.crawl_schedulers.CrawlScheduler:
        return DispatchCallLogSpider._crawl_scheduler

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import NewsBot.items.dispatch


class DispatchCallLogSpider(scrapy.Spider):
    name            = 'DispatchCallLogSpider'
    allowed_domains = ['edispatches.com']
    _DISPATCH_LOG_ROW           = "//*[@id='call-log-info']//table/tr"
    _DISPATCH_AUDIO_RELATIVE_XPATH      = "./td[1]/audio/@src"
    _DISPATCHED_AGENCY_RELATIVE_XPATH   = "./td[2]/text()"
    _DISPATCH_TIME_RELATIVE_XPATH       = "./td[4]/text()"
    
    def start_requests(self):
        return [
            scrapy.FormRequest(
                "https://www.edispatches.com/call-log/index.php",
                formdata    = {
                    "ddl-state":    "UT",
                    "ddl-county":   "Grand",
                    "ddl-company":  "ALL",
                    "ddl-limit":    "ALL",
                },
                callback    = self.parse_call_log,
            )
        ]

    def parse_call_log(self, response: scrapy.http.HtmlResponse):
        allDispatchLogRows = response.xpath(self._DISPATCH_LOG_ROW)
        allDispatches = [
            NewsBot.items.Dispatch(
                audio_URL           = oneRow.xpath(self._DISPATCH_AUDIO_RELATIVE_XPATH).get(),
                dispatched_agency   = oneRow.xpath(self._DISPATCHED_AGENCY_RELATIVE_XPATH).get(),
                time_string         = oneRow.xpath(self._DISPATCH_TIME_RELATIVE_XPATH).get(),
            )
            for oneRow in allDispatchLogRows
        ]
        return allDispatches

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.http
import NewsBot.spiders.self_scheduling_spider
import NewsBot.items.frontier_investigation_filing
import newsbot_tasking.crawl_schedulers.uniformly_random_scheduler
import newsbot_tasking.crawl_schedulers.crawl_scheduler
import datetime


class FrontierInvestigationSpider(
    NewsBot.spiders.self_scheduling_spider.SelfSchedulingSpider,
    NewsBot.logger.Logger,
):
    # name =              __name__
    allowed_domains =   ["utah.gov"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "NewsBot.item_pipelines.emailed_item_filter.EmailedItemFilter":                 10,
            "NewsBot.item_pipelines.file_downloader.FileDownloader":                        100,
            "NewsBot.item_pipelines.dispatch_datetime_cruncher.DispatchDatetimeCruncher":   200,
            "NewsBot.item_pipelines.item_emailer.ItemEmailer":                              500,
        }
    }
    
    def __init__(self):
        self._filing_xpath =                    "//main//table//tr[position()>1]"
        self._filing_date_relative_xpath =      "./td[1]/text()"
        self._documents_relative_xpath =        "./td[2]/a"
        self._document_description_relative_xpath =    "./text()"
        self._document_url_relative_xpath =     "./@href"
        
        self._crawl_scheduler = (
            newsbot_tasking.crawl_schedulers.uniformly_random_scheduler.UniformlyRandomScheduler(
                maximum_interval =  datetime.timedelta(minutes = 25),
                minimum_interval =  datetime.timedelta(minutes = 15),
            )
        )
        
        super().__init__()
    
    def start_requests(self) -> [scrapy.http.Request]:
        return [
            scrapy.Request(
                "https://psc.utah.gov/2019/05/20/docket-no-19-041-04/",
                callback =  self.parse_filing_table,
            )
        ]

    def parse_filing_table(self,
        response: scrapy.http.HtmlResponse
    ) -> [NewsBot.items.frontier_investigation_filing.FrontierInvestigationFiling]:
        raise NotImplementedError

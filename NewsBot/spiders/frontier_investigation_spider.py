# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.http
import newsbot.spiders.self_scheduling_spider as self_scheduling_spider
import newsbot.items.frontier_investigation_filing as frontier_investigation_filing
import newsbot.tasking.crawl_schedulers.uniformly_random_scheduler as uniformly_random_scheduler
import newsbot.tasking.crawl_schedulers.crawl_scheduler as crawl_scheduler
import newsbot.logger as logger
import datetime
import scrapy.selector


class FrontierInvestigationSpider(
    self_scheduling_spider.SelfSchedulingSpider,
    logger.Logger,
):
    name =              __name__
    allowed_domains =   ["utah.gov"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "NewsBot.item_pipelines.emailed_item_filter.EmailedItemFilter":     10 ,
            "NewsBot.item_pipelines.file_downloader.FileDownloader":            400,
            "NewsBot.item_pipelines.datetime_cruncher.DatetimeCruncher":        500,
            "NewsBot.item_pipelines.item_emailer.ItemEmailer":                  900,
            "NewsBot.item_pipelines.emailed_item_recorder.EmailedItemRecorder": 990,
        },
        "MEDIA_ALLOW_REDIRECTS": True,
    }
    
    def __init__(self):
        self._filing_xpath =                    "//main//table//tr[position()>1]"
        self._filing_date_relative_xpath =      "./td[1]/text()"
        self._documents_relative_xpath =        "./td[2]/a"
        self._document_description_relative_xpath =    "./text()"
        self._document_url_relative_xpath =     "./@href"
        
        self._crawl_scheduler = (
            uniformly_random_scheduler.UniformlyRandomScheduler(
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
    ) -> [frontier_investigation_filing.FrontierInvestigationFiling]:
        all_filing_rows = response.xpath(self._filing_xpath)
        all_filings = [
            frontier_investigation_filing.FrontierInvestigationFiling(
                file_URLs = (
                    one_row.xpath(
                        self._documents_relative_xpath
                    ).xpath(
                        self._document_url_relative_xpath
                    ).getall()
                ),
                source_date_string =    one_row.xpath(self._filing_date_relative_xpath).get(),
                source_date_format =    "%B %d, %Y",
                filing_name_map =       self._extract_name_map(one_row),
            )
            for one_row in all_filing_rows
        ]
        return all_filings
    
    def _extract_name_map(self,
        filing_row: scrapy.selector.Selector,
    ):
        return {
            each_doc.xpath(self._document_description_relative_xpath).get():
            each_doc.xpath(self._document_url_relative_xpath).get()
            for each_doc
            in filing_row.xpath(self._documents_relative_xpath)
        }

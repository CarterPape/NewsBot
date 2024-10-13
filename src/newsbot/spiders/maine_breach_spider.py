# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import collections.abc
import zoneinfo
import scrapy
import scrapy.http
import scrapy.crawler
import scrapy.selector
from newsbot.spiders import self_scheduling_spider
from newsbot.items import maine_breach
from newsbot.tasking.crawl_schedulers import time_conditional_scheduler
from newsbot.db_connections import \
    emailed_items_db_connection, \
    filtered_breaches_db_connection, \
    bank_breaches_db_connection


class MaineBreachSpider(self_scheduling_spider.SelfSchedulingSpider):
    name =              __name__
    allowed_domains =   ["maine.gov"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "newsbot.item_pipelines.emailed_item_filter.EmailedItemFilter":     10 ,
            "newsbot.item_pipelines.file_downloader.FileDownloader":            400,
            "newsbot.item_pipelines.item_emailer.ItemEmailer":                  900,
            "newsbot.item_pipelines.emailed_item_recorder.EmailedItemRecorder": 901,
        },
        "MEDIA_ALLOW_REDIRECTS": True,
    }
    
    @classmethod
    def make_a_scheduler(klass, *,
        from_crawler: scrapy.crawler.Crawler,
        suggested_scheduler = None
    ):
        new_scheduler = time_conditional_scheduler.TimeConditionalScheduler(
            working_timezone = zoneinfo.ZoneInfo("America/New_York")
        )
        
        return super().make_a_scheduler(
            from_crawler = from_crawler,
            suggested_scheduler = suggested_scheduler or new_scheduler
        )
    
    def __init__(self):
        self._disclosure_xpath = "//body//div[@id='maincontent3']/table/tbody/tr"
        self._reported_date_relative_xpath = "./td[1]/text()"
        
        self._details_relative_xpath = "./td[2]/a"
        self._organization_relative_xpath = "./td[2]/a/text()"
        self._details_url_relative_xpath = "./td[2]/a/@href"
        
        self._org_type_xpath = "//*[@id='maincontent3']/ul[1]/li[1]/strong/text()"
        self._people_affected_xpath = "//*[@id='maincontent3']/ul[3]/li[1]/strong/text()"
        
        self._occurred_date_xpath = '//*[@id="maincontent3"]/ul[3]/li[4]/strong/text()'
        self._discovery_date_xpath = '//*[@id="maincontent3"]/ul[3]/li[5]/strong/text()'
        self._consumer_notification_date_xpath = '//*[@id="maincontent3"]/ul[4]/li[2]/strong/text()'
        
        self._breached_information_xpath = '//*[@id="maincontent3"]/ul[3]/li[7]/strong/text()'
        self._provided_description_xpath = '//*[@id="maincontent3"]/ul[3]/li[6]/ul'
        
        self._submitter_name_xpath = '//*[@id="maincontent3"]/ul[2]/li[1]/strong/text()'
        self._submitter_relationship_xpath = '//*[@id="maincontent3"]/ul[2]/li[6]/strong/text()'
        self._submitter_email_xpath = '//*[@id="maincontent3"]/ul[2]/li[5]/strong/text()'
        self._submitter_phone_number_xpath = '//*[@id="maincontent3"]/ul[2]/li[4]/strong/text()'
        
        self._consumer_notice_url_xpath = '//*[@id="maincontent3"]/ul[4]/li[3]/strong/a/@href'
        
        self._breach_exclusion_db_connection: \
            filtered_breaches_db_connection.FilteredBreachesDBConnection
        self._bank_breach_db_connection: bank_breaches_db_connection.BankBreachesDBConnection
        self._emailed_items_db_connection: emailed_items_db_connection.EmailedItemsDBConnection
        
        super().__init__()
    
    def start_requests(self) -> list[scrapy.http.Request]:
        self._breach_exclusion_db_connection = \
            filtered_breaches_db_connection.FilteredBreachesDBConnection(
                settings = self.settings
            )
        self._bank_breach_db_connection = bank_breaches_db_connection.BankBreachesDBConnection(
            settings=self.settings
        )
        self._emailed_items_db_connection = emailed_items_db_connection.EmailedItemsDBConnection(
            settings = self.settings
        )
        
        return [
            scrapy.Request(
                "https://apps.web.maine.gov/online/aeviewer/ME/40/list.shtml",
                callback =  self._parse_disclosure_table,
            )
        ]
    
    def _parse_disclosure_table(self,
        response: scrapy.http.HtmlResponse,
    ) -> collections.abc.Iterable[scrapy.Request]:
        all_disclosure_rows = response.xpath(self._disclosure_xpath)
        
        for each_disclosure in all_disclosure_rows:
            each_breach = maine_breach.MaineBreach(
                details_url = response.urljoin(
                    each_disclosure.xpath(self._details_url_relative_xpath).get()
                ),
                organization_name = each_disclosure.xpath(self._organization_relative_xpath).get(),
                reported_date = each_disclosure.xpath(self._reported_date_relative_xpath).get(),
            )
            
            if (
                (
                    not self._breach_exclusion_db_connection.is_breach_excluded(each_breach)
                ) and (
                    self._emailed_items_db_connection.datetime_item_transmitted(each_breach) is None
                )
            ):
                yield scrapy.Request(
                    each_breach['details_url'],
                    callback = self._parse_details_page,
                    cb_kwargs = {
                        "breach_partial": each_breach
                    }
                )
    
    def _parse_details_page(self,
        response: scrapy.http.HtmlResponse,
        *,
        breach_partial: maine_breach.MaineBreach,
    ) -> maine_breach.MaineBreach | list:
        breach_partial['org_type'] = response.xpath(self._org_type_xpath).get()
        breach_partial['people_affected'] = response.xpath(self._people_affected_xpath).get()
        
        if self._include_breach(breach_partial):
            breach_partial['occurred_date'] = response.xpath(self._occurred_date_xpath).get()
            breach_partial['discovery_date'] = response.xpath(self._discovery_date_xpath).get()
            breach_partial['consumer_notification_date'] = (
                response.xpath(self._consumer_notification_date_xpath).get()
            )
            
            breach_partial['breached_information'] = (
                response.xpath(self._breached_information_xpath).get()
            )
            breach_partial['provided_description'] = (
                response.xpath(self._provided_description_xpath).get()
            )
            
            breach_partial['submitter_name'] = response.xpath(self._submitter_name_xpath).get()
            breach_partial['submitter_relationship'] = (
                response.xpath(self._submitter_relationship_xpath).get()
            )
            breach_partial['submitter_email'] = response.xpath(self._submitter_email_xpath).get()
            breach_partial['submitter_phone_number'] = (
                response.xpath(self._submitter_phone_number_xpath).get()
            )
            
            breach_partial['file_URLs'] = [response.urljoin(
                response.xpath(self._consumer_notice_url_xpath).get()
            )]
            
            if not self._bank_breach_db_connection.is_breach_recorded(breach_partial):
                self._bank_breach_db_connection.record_breach(breach_partial)
            
            return breach_partial
        
        self._breach_exclusion_db_connection.record_breach_exclusion(breach_partial)
        return []
    
    @staticmethod
    def _include_breach(breach_partial: maine_breach.MaineBreach) -> bool:
        return str.casefold(breach_partial['org_type']) == str.casefold("Financial Services")

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import logging
import scrapy
import scrapy.http
import scrapy.crawler
import newsbot.spiders.self_scheduling_spider as self_scheduling_spider
import newsbot.items.frontier_investigation_filing as frontier_investigation_filing
import newsbot.tasking.crawl_schedulers.uniformly_random_scheduler as uniformly_random_scheduler
import newsbot.tasking.crawl_schedulers.crawl_scheduler as crawl_scheduler
import newsbot.db_connections.news_articles_db_connection as news_articles_db_connection
import newsbot.db_connections.news_sources_db_connection as news_sources_db_connection
import newsbot.items.news_source as news_source
import newsbot.items.news_article as news_article
import datetime
import pytz
import scrapy.selector


class NewsSourceSpider(self_scheduling_spider.SelfSchedulingSpider):
    name = __name__
    custom_settings = {
        "ITEM_PIPELINES": {
            "newsbot.item_pipelines.open_graph_extractor.OpenGraphExtractor":   100,
            "newsbot.item_pipelines.item_emailer.ItemEmailer":                  900,
            "newsbot.item_pipelines.emailed_item_recorder.EmailedItemRecorder": 910,
        },
    }
    
    @classmethod
    def make_a_scheduler(klass, *,
        from_crawler: scrapy.crawler.Crawler,
        suggested_scheduler = None
    ):
        new_scheduler = (
            uniformly_random_scheduler.UniformlyRandomScheduler(
                maximum_interval =  datetime.timedelta(minutes = 15),
                minimum_interval =  datetime.timedelta(minutes = 5),
            )
        )
        
        return super().make_a_scheduler(
            from_crawler = from_crawler,
            suggested_scheduler = suggested_scheduler or new_scheduler
        )
    
    def __init__(self):
        self._news_sources_db_connection:   news_sources_db_connection.NewsSourcesDBConnection
        self._news_articles_db_connection:  news_articles_db_connection.NewsArticlesDBConnection
        
        super().__init__()
    
    def start_requests(self) -> typing.List[scrapy.http.Request]:
        self._news_sources_db_connection =  news_sources_db_connection.NewsSourcesDBConnection(
            settings = self.settings,
        )
        self._news_articles_db_connection = news_articles_db_connection.NewsArticlesDBConnection(
            settings = self.settings,
        )
        
        news_source_list = self._news_sources_db_connection.get_source_list()
        
        for news_source in news_source_list:
            yield scrapy.Request(
                news_source.url,
                callback =  self.parse_article_list,
                cb_kwargs = {
                    "the_source": news_source,
                }
            )
    
    def parse_article_list(self,
        response: scrapy.http.HtmlResponse,
        *,
        the_source: news_source.NewsSource,
    ) -> typing.List[news_article.NewsArticle]:
        
        all_urls = response.xpath(the_source.links_xpath)
        
        logging.info(f"Found {len(all_urls)} articles on {the_source}")
        
        for one_article_url in all_urls:
            yield news_article.NewsArticle(
                article_url = one_article_url.get(),
            )

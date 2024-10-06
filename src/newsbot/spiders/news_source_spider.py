# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import collections.abc
import logging
import urllib.parse
import datetime

import scrapy
import scrapy.http
import scrapy.crawler
import scrapy.selector

from newsbot.spiders import self_scheduling_spider
from newsbot.tasking.crawl_schedulers import uniformly_random_scheduler
from newsbot.db_connections import news_articles_db_connection
from newsbot.db_connections import news_sources_db_connection
from newsbot.items import news_source
from newsbot.items import news_article


class NewsSourceSpider(self_scheduling_spider.SelfSchedulingSpider):
    name = __name__
    custom_settings = {
        "ITEM_PIPELINES": {
            "newsbot.item_pipelines.emailed_item_filter.EmailedItemFilter":     10 ,
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
                maximum_interval =  datetime.timedelta(minutes = 20),
                minimum_interval =  datetime.timedelta(minutes = 15),
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
    
    def start_requests(self) -> collections.abc.Iterable[scrapy.http.Request]:
        self._news_sources_db_connection =  news_sources_db_connection.NewsSourcesDBConnection(
            settings = self.settings,
        )
        self._news_articles_db_connection = news_articles_db_connection.NewsArticlesDBConnection(
            settings = self.settings,
        )
        
        news_source_list = self._news_sources_db_connection.list_all_sources()
        
        for each_news_source in news_source_list:
            for each_search_url in each_news_source.search_url_list:
                yield scrapy.Request(
                    each_search_url,
                    method = each_news_source.request_method,
                    headers = each_news_source.request_headers,
                    callback =  self.parse_article_list,
                    cb_kwargs = {
                        "the_source": each_news_source,
                    },
                )
    
    def parse_article_list(self,
        response: scrapy.http.HtmlResponse,
        *,
        the_source: news_source.NewsSource,
    ) -> collections.abc.Iterable[news_article.NewsArticle]:
        
        all_urls = the_source.links_parser.parse_response(response)
        
        if len(all_urls) > 0:
            logging.info(f"Found {len(all_urls)} articles on {the_source}")
        else:
            logging.warning(f"Found no articles on {the_source}")
        
        for each_article_url in all_urls:
            yield news_article.NewsArticle(
                clean_url = self._clean_url(
                    dirty_url = each_article_url
                ),
                news_source = the_source,
                search_url = response.url,
            )
    
    def _clean_url(self, *,
        dirty_url: str,
    ):
        parsed_url = urllib.parse.urlparse(dirty_url)
        
        clean_url = urllib.parse.urlunparse(
            parsed_url._replace(
                query = "",
                params = "",
                fragment = "",
            )
        )
        
        logging.debug(f"Cleaned url {dirty_url} into {clean_url}")
        
        return clean_url

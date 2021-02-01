# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import logging
import scrapy.settings
import newsbot.db_connections.db_connection as db_connection
import newsbot.db_connections.helpers.news_sources_definitions as news_sources_definitions
import newsbot.items.news_article as news_article
import newsbot.items.news_source as news_source
import datetime
import newsbot.exceptions.duplicate_entry_exception as duplicate_entry_exception


class NewsSourcesDBConnection(db_connection.DBConnection):
    def __init__(self, *args, **kwargs,):
        self._news_sources: dict[str, news_source.NewsSource]
    
    @property
    def table_name(self) -> str:
        return "news_sources (a faux table)"
    
    @property
    def table_definition(self) -> str:
        raise RuntimeError("No MySQL table is defined for news sources. For now, news sources are defined and maintained in code.")
    
    def table_exists(self) -> bool:
        logging.debug(f"No MySQL table is defined for news sources. For now, checking whether the list of news sources has been loaded into memory.")
        
        return self._news_sources != None
    
    def create_table(self):
        logging.info(f"Loading the list of news sources into memory")
        
        self._news_sources = news_sources_definitions.NewsSourcesDefinitions.list_all_sources()
    
    def list_all_sources(self) -> dict[str, news_source.NewsSource]:
        return self._news_sources

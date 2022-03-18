# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import typing
import logging

from newsbot.db_connections import db_connection
from newsbot.db_connections.helpers import news_sources_definitions
from newsbot.items import news_source


class NewsSourcesDBConnection(db_connection.DBConnection):
    @property
    def table_name(self) -> str:
        return "news_sources (a faux table)"
    
    @property
    def table_definition(self) -> str:
        raise RuntimeError(
            "No MySQL table is defined for news sources. "
            "For now, news sources are defined and maintained in code."
        )
    
    def table_exists(self) -> bool:
        logging.debug(
            "No MySQL table is defined for news sources. "
            "For now, checking whether the list of news sources can be loaded into memory."
        )
        
        return (
            len(
                news_sources_definitions.NewsSourcesDefinitions.list_all_sources()
            ) > 0
        )
    
    def create_table(self):
        raise RuntimeError(
            "No MySQL table is defined for news sources."
            "For now, news sources are defined and maintained in code."
        )
    
    def list_all_sources(self) -> typing.List[news_source.NewsSource]:
        return news_sources_definitions.NewsSourcesDefinitions.list_all_sources()

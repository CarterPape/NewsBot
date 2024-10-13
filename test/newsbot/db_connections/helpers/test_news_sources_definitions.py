# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

from newsbot.db_connections.helpers import news_sources_definitions
from newsbot.items import news_source
from newsbot.spiders.helpers import link_list_parser

def test_news_sources_definitions():
    news_sources_definitions.NewsSourcesDefinitions.list_all_sources()
    for each_news_source in news_sources_definitions.NewsSourcesDefinitions.list_all_sources():
        assert each_news_source.source_id
        assert isinstance(each_news_source.links_parser, link_list_parser.LinkListParser)
        assert isinstance(each_news_source, news_source.NewsSource)

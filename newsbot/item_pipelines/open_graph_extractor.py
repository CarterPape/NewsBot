# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import metadata_parser

from newsbot.items import news_article
from newsbot.item_pipelines import item_pipeline

class OpenGraphExtractor(item_pipeline.ItemPipeline):
    def process_item(self,
        item:   news_article.NewsArticle,
        spider: scrapy.spiders.Spider,
    ) -> news_article.NewsArticle:
        
        page_data = metadata_parser.MetadataParser(
            url = item["clean_url"],
            search_head_only = True,
        )
        item["title"] =         (page_data.get_metadatas("title") or [None])[0]
        item["description"] =   (page_data.get_metadatas("description") or [None])[0]
        item["img_src"] =       (page_data.get_metadatas("image") or [None])[0]
        
        return item

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2021 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import scrapy
import newsbot.items.news_article as news_article
import newsbot.item_pipelines.item_pipeline as item_pipeline
import metadata_parser

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

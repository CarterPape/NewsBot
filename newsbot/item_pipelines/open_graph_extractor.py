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

class OpenGraphExtractor(item_pipeline.ItemPipeline):
    def process_item(self,
        item:   news_article.NewsArticle,
        spider: scrapy.spiders.Spider,
    ) -> news_article.NewsArticle:
        print(item['clean_url'])
        raise scrapy.exceptions.DropItem("Skipping for now")

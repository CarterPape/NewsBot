# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging

import scrapy

from newsbot.items import emailable_item
from newsbot.item_pipelines import item_pipeline
from newsbot.db_connections import emailed_items_db_connection


class EmailedItemRecorder(item_pipeline.ItemPipeline):
    def process_item(
        self,
        item: emailable_item.EmailableItem,
        spider: scrapy.Spider
    ) -> emailable_item.EmailableItem:
        
        logging.debug(f"Recording item {item} as emailed")
        db_connection = emailed_items_db_connection.EmailedItemsDBConnection(
            settings = spider.settings,
        )
        db_connection.record_emailed_item(item)
        db_connection.close()

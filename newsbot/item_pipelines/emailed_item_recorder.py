# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import logging
import newsbot.items.emailable_item as emailable_item
import newsbot.item_pipelines.item_pipeline as item_pipeline
import newsbot.db_connections.emailed_items_db_connection as emailed_items_db_connection


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

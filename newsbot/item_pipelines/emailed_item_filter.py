# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import logging
import typing
import newsbot.items.emailable_item as emailable_item
import newsbot.item_pipelines.item_pipeline as item_pipeline
import newsbot.db_connections.emailed_items_db_connection as emailed_items_db_connection
import newsbot.exceptions.drop_transmitted_item as drop_transmitted_item
import newsbot.exceptions.drop_duplicate_item as drop_duplicate_item


class EmailedItemFilter(item_pipeline.ItemPipeline):
    def __init__(self):
        self._serialized_items_seen: typing.Set[str] = set()
    
    def process_item(
        self,
        item: emailable_item.EmailableItem,
        spider: scrapy.Spider
    ) -> emailable_item.EmailableItem:
        
        serialized_item = item.serialized()
        
        if serialized_item in self._serialized_items_seen:
            raise drop_duplicate_item.DropDuplicateItem(
                f"Item ({item}) seen earlier this session"
            )
        else:
            self._serialized_items_seen.add(serialized_item)
        
        db_connection = emailed_items_db_connection.EmailedItemsDBConnection(
            settings = spider.settings
        )
        datetime_transmitted = db_connection.datetime_item_transmitted(item)
        db_connection.close()
        
        if datetime_transmitted == None:
            logging.debug(f"Item {item} has not been emailed previously.")
            return item
        else:
            raise drop_transmitted_item.DropTransmittedItem(
                f"Item ({item}) already successfully emailed {datetime_transmitted}"
            )

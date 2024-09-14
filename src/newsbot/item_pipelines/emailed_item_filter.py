# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import typing

import scrapy

from newsbot.items import emailable_item
from newsbot.item_pipelines import item_pipeline
from newsbot.db_connections import emailed_items_db_connection
from newsbot.exceptions import drop_transmitted_item
from newsbot.exceptions import drop_duplicate_item


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
        
        if datetime_transmitted is None:
            logging.debug(f"Item {item} has not been emailed previously.")
            return item
        else:
            raise drop_transmitted_item.DropTransmittedItem(
                f"Item ({item}) already successfully emailed {datetime_transmitted}"
            )

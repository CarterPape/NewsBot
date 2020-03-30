# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import newsbot.items.emailable_item as emailable_item
import newsbot.item_pipelines.item_pipeline as item_pipeline
import newsbot.db_connections.emailed_items_db_connection as emailed_items_db_connection
import newsbot.exceptions.drop_transmitted_item as drop_transmitted_item


class EmailedItemFilter(item_pipeline.ItemPipeline):
    def process_item(
        self,
        item: emailable_item.EmailableItem,
        spider: scrapy.Spider
    ) -> emailable_item.EmailableItem:
        
        db_connection = emailed_items_db_connection.EmailedItemsDBConnection(
            settings = spider.settings
        )
        datetime_transmitted = db_connection.datetime_item_transmitted(item)
        db_connection.close()
        
        if datetime_transmitted == None:
            return item
        else:
            raise drop_transmitted_item.DropTransmittedItem(
                f"Item ({item}) already successfully emailed {datetime_transmitted}"
            )

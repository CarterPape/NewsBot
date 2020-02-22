# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import NewsBot.items.emailable_item
import NewsBot.spiders
import NewsBot.item_pipelines.item_pipeline
import scrapy.spiders
import NewsBot.db_connections.emailed_items_db_connection as emailed_items_db_connection
import NewsBot.exceptions.drop_transmitted_item as drop_transmitted_item


class EmailedItemFilter(NewsBot.item_pipelines.item_pipeline.ItemPipeline):
    def process_item(
        self,
        item: NewsBot.items.emailable_item.EmailableItem,
        spider: scrapy.spiders.Spider
    ) -> NewsBot.items.emailable_item.EmailableItem:
        
        db_connection = emailed_items_db_connection.EmailedItemsDBConnection()
        datetime_transmitted = db_connection.datetime_item_transmitted(item)
        db_connection.close()
        
        if datetime_transmitted == None:
            return item
        else:
            raise drop_transmitted_item.DropTransmittedItem(
                f"Item ({item}) already successfully emailed {datetime_transmitted}"
            )

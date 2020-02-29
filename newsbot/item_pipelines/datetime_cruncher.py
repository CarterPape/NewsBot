# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import datetime
import pytz
import newsbot.items.dated_item as dated_item
import newsbot.item_pipelines.item_pipeline as item_pipeline


class DatetimeCruncher(item_pipeline.ItemPipeline):
    def __init__(self):
        if not hasattr(self, "source_timezone"):
            self._source_timezone = pytz.timezone("America/Denver")
    
    def process_item(
        self,
        item:   dated_item.DatedItem,
        spider: scrapy.Spider
    ) -> dated_item.DatedItem:
        
        item["datetime"] = datetime.datetime.strptime(
            item["source_date_string"],
            item["source_date_format"],
        )
        item["datetime"] = self._source_timezone.localize(item["datetime"])
        return item

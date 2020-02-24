# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import scrapy.spiders
import datetime
import NewsBot.items.dispatch
import NewsBot.spiders
import NewsBot.item_pipelines.item_pipeline as item_pipeline
import logging
import datetime
import pytz


class DatetimeCruncher(item_pipeline.ItemPipeline):
    def __init__(self):
        if not hasattr(self, "source_timezone"):
            self._source_timezone = pytz.timezone("America/Denver")
    
    def process_item(
        self,
        item: NewsBot.items.dispatch.Dispatch,
        spider: scrapy.spiders.Spider
    ) -> NewsBot.items.dispatch.Dispatch:
        
        item["datetime"] = datetime.datetime.strptime(
            item["source_date_string"],
            item["source_date_format"],
        )
        item["datetime"] = self._source_timezone.localize(item["datetime"])
        return item

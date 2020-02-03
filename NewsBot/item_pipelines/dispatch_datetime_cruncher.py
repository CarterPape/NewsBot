# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import datetime
import NewsBot.items
import NewsBot.spiders
import logging
import datetime
import pytz

class DispatchDatetimeCruncher(object):
    _SOURCE_DATETIME_FORMAT     = "%Y-%m-%d %H:%M:%S"
    _SOURCE_TIMEZONE            = pytz.timezone('America/Denver')
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    
    def process_item(
        self,
        item: NewsBot.items.Dispatch,
        spider: NewsBot.spiders.DispatchCallLogSpider
    ) -> NewsBot.items.Dispatch:
        
        item["dispatch_datetime"] = datetime.datetime.strptime(
            item["dispatch_date_string"],
            self._SOURCE_DATETIME_FORMAT,
        )
        item["dispatch_datetime"] = self._SOURCE_TIMEZONE.localize(item["dispatch_datetime"])
        return item
        

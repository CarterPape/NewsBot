# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import NewsBot.items
import NewsBot.spiders
import scrapy
import scrapy.settings
import os
import string
import os.path
import magic
import requests
import keyring
import dotenv
import pape.utilities
import typing
import twisted


class ItemPipeline(NewsBot.logger.Logger):
    def __init__(self):
        pass
        
    def process_item(self,
        item:   scrapy.item.Item,
        spider: scrapy.spiders.Spider,
    ) -> typing.Union[
        scrapy.Item,
        dict,
        twisted.internet.defer.Deferred,
    ]:
        raise NotImplementedError
    
    def open_spider(self,
        spider: scrapy.spiders.Spider
    ):
        pass
    
    def close_spider(self,
        spider: scrapy.spiders.Spider
    ):
        pass

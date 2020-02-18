# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy.item
import json


class ItemWithFiles(scrapy.item.Item):
    file_URLs = scrapy.item.Field()
    files =     scrapy.item.Field(ignore_when_serializing = True)
    
    @classmethod
    def get_files_urls_field(klass) -> str:
        return "file_URLs"
    
    @classmethod
    def get_files_result_field(klass) -> str:
        return "files"

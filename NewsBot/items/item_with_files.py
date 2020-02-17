# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy


class ItemWithFiles(scrapy.Item):
    file_URLs = scrapy.Field()
    files =     scrapy.Field(serializer = None)
    
    @classmethod
    def get_files_urls_field(klass) -> str:
        return "file_URLs"
    
    @classmethod
    def get_files_result_field(klass) -> str:
        return "files"

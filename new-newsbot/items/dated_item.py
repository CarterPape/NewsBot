# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy


class DatedItem(scrapy.Item):
    source_date_string =    scrapy.Field()
    source_date_format =    scrapy.Field(ignore_when_serializing = True)
    datetime =              scrapy.Field(ignore_when_serializing = True)

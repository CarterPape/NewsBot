# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy


class NewsSource(scrapy.Item):
    source_id =     scrapy.Field(ignore_when_serializing = True)
    url =           scrapy.Field()
    name =          scrapy.Field()
    links_xpath =   scrapy.Field()

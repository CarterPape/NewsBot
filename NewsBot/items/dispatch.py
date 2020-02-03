# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Dispatch(scrapy.Item):
    audio_URL           = scrapy.Field()
    audio_file_path     = scrapy.Field()
    dispatched_agency   = scrapy.Field()
    dispatch_date_string    = scrapy.Field()
    dispatch_datetime   = scrapy.Field() 

# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import abc


class DatedItem(
    scrapy.Item,
    metaclass = abc.ABCMeta,
):
    source_date_string =    scrapy.Field()
    source_date_format =    scrapy.Field(ignore_when_serializing = True)
    datetime =              scrapy.Field(ignore_when_serializing = True)

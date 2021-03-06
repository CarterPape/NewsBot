# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import scrapy
import typing
import twisted
import abc


class ItemPipeline(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def process_item(self,
        item:   scrapy.Item,
        spider: scrapy.Spider,
    ) -> typing.Union[
        scrapy.Item,
        dict,
        twisted.internet.defer.Deferred,
    ]:
        pass

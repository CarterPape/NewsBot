# # # # # # # # # # # # # # # # # # # #
# NewsBot, a journalism tool
# Copyright 2020 Carter Pape
# 
# See file LICENSE for licensing terms.
# # # # # # # # # # # # # # # # # # # #

import logging
import scrapy.logformatter
import NewsBot.exceptions.drop_transmitted_item


class NewsBotLogFormatter(scrapy.logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        if exception is NewsBot.exceptions.drop_transmitted_item.DropTransmittedItem:
            return {
                "level":    logging.INFO,
                "msg":      scrapy.logformatter.DROPPEDMSG,
                "args": {
                    "exception":    exception,
                    "item":         item,
                },
            }
        else:
            return super().dropped(
                item,
                exception,
                response,
                spider,
            )
